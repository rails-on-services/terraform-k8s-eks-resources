
output "istio_ingressgateway_alb" {
  value = kubernetes_ingress.istio-alb-ingressgateway
}
