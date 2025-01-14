resource "kubernetes_deployment" "ml_model" {
  metadata {
    name      = "ml-model"
    namespace = kubernetes_namespace.aikube.metadata[0].name
    labels = {
      app = "ml-model"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "ml-model"
      }
    }

    template {
      metadata {
        labels = {
          app = "ml-model"
        }
      }

      spec {
        container {
          name  = "ml-model"
          image = "localhost:5002/aikube-ml_model:latest"
          image_pull_policy = "Never"  # Use local images

          port {
            container_port = 5001
          }

          resources {
            limits = {
              cpu    = "1"
              memory = "1Gi"
            }
            requests = {
              cpu    = "500m"
              memory = "512Mi"
            }
          }

          liveness_probe {
            http_get {
              path = "/"
              port = 5001
            }
            initial_delay_seconds = 30
            period_seconds       = 10
          }
        }
      }
    }
  }
}


resource "kubernetes_service" "ml_model" {
  metadata {
    name      = "ml-model-service"
    namespace = kubernetes_namespace.aikube.metadata[0].name
  }

  spec {
    selector = {
      app = "ml-model"
    }

    port {
      port        = 80
      target_port = 5001
    }

    type = "ClusterIP"
  }
}