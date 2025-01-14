resource "docker_container" "local_registry" {
  name  = "local-registry"
  image = "registry:2"

  ports {
    internal = 5000
    external = 5002
  }

  healthcheck {
    test         = ["CMD", "curl", "-f", "http://localhost:5000/v2/"]
    interval     = "5s"
    timeout      = "3s"
    start_period = "5s"
    retries      = 3
  }

  restart = "unless-stopped"

  must_run = true
}