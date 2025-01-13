# Namespaces help organise and isolate resources in Kubernetes.
resource "kubernetes_namespace" "aikube" {
  metadata {
    name = "aikube-namespace"
  }
}
