resource "kubernetes_persistent_volume" "fastapi_logs" {
  metadata {
    name = "fastapi-logs-pv"
  }

  spec {
    capacity = {
      storage = "1Gi"
    }

    access_modes = ["ReadWriteOnce"]

    persistent_volume_source {
      host_path {
        path = "/mnt/data/fastapi-logs"  # Host directory for logs
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim" "fastapi_logs_pvc" {
  metadata {
    name      = "fastapi-logs-pvc"
    namespace = kubernetes_namespace.aikube.metadata[0].name
  }

  spec {
    access_modes = ["ReadWriteOnce"]

    resources {
      requests = {
        storage = "1Gi"
      }
    }
  }
}
