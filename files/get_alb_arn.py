#!/usr/bin/env python3
import subprocess
import os
import json
import sys
import time

def external_data():
  # Make sure the input is a valid JSON.
  input_json = sys.stdin.read()
  try:
      input_dict = json.loads(input_json)
  except ValueError as value_error:
      sys.exit(value_error)

  # AWS profile
  aws_profile=input_dict["aws_profile"]

  # Generate kubeconfig file
  kubeconfig = input_dict["kubeconfig"]
  f = open("kube_config.yaml", "w")
  f.write(kubeconfig)
  f.close()

  hostname = None
  tries = 100
  for i in range(tries):
    try:
      # Get istio load balancer hostname attached to our cluster
      hostname=subprocess.check_output(['kubectl', '--kubeconfig', \
          'kube_config.yaml', \
          '-n', 'istio-system', \
          'get', 'ingress', \
          'istio-alb-ingressgateway', \
          '-o', 'jsonpath={.status.loadBalancer.ingress[*].hostname}']).decode('utf-8')
      loadbalancers=subprocess.check_output(['aws', 'elbv2', \
        'describe-load-balancers', \
        '--profile', '{}'.format(aws_profile), \
        '--query', 'LoadBalancers[*]', \
        '--output', 'json'])
      json_lb = json.loads(loadbalancers)
      # Look for LB that matches istio LB hostname, output first match
      match_lb = list(filter(lambda x: x['DNSName'] == hostname and x['State']['Code'] == 'active', json_lb))
      if not match_lb:
        raise Exception("No lb found")
      lb = match_lb[0]
      sys.stdout.write(json.dumps({"LoadBalancerArn": lb["LoadBalancerArn"]}))
      sys.exit()
    except Exception:
      if i < tries - 1: # i is zero indexed
        time.sleep(1)
        continue
    break

  error_output()

def error_output(error=""):
  sys.stderr.write(error)
  sys.exit(1)

if __name__ == "__main__":
  external_data()