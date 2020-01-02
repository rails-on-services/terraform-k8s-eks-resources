clusterName: ${cluster_name}
autoDiscoverAwsRegion: true
autoDiscoverAwsVpcID: true
aws-vpc-id: ${vpc_id}
aws-region: ${aws_region}
image:
  tag: v1.1.2
enableReadinessProbe: true
enableLivenessProbe: true
resources:
  requests:
    cpu: 0.3
    memory: 512Mi
scope:
  ingressClass: alb
extraArgs:
  feature-gates: 'waf=false'
