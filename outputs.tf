
output "istio_ingressgateway_alb_arn" {
  value = data.external.alb_arn.result.LoadBalancerArn
}
