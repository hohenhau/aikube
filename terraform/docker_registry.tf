resource "docker_container" "local_registry" {
  name  = "local-registry"
  image = "registry:2"
  ports {
    internal = 5000
    external = 5002
  }
}
