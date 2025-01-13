resource "kubernetes_deployment" "fastapi_app" {
  metadata {
    name      = "fastapi-app"
    namespace = kubernetes_namespace.aikube.metadata[0].name
    labels = {
      app = "fastapi-app"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "fastapi-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "fastapi-app"
        }
      }

      spec {
        container {
          name  = "fastapi-app"
          image = "localhost:5002/aikube-fastapi_app:latest"

          port {
            container_port = 8000
          }

          env {
            name  = "ML_MODEL_URL"
            value = "http://ml-model-service:80"
          }

          env {
            name  = "DATABASE_URL"
            value = "postgresql://test_user:test_password@postgres:5432/test_db"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "fastapi_app" {
  metadata {
    name      = "fastapi-service"
    namespace = kubernetes_namespace.aikube.metadata[0].name
  }

  spec {
    selector = {
      app = "fastapi-app"
    }

    port {
      port        = 80
      target_port = 8000
    }

    type = "NodePort"
  }
}
