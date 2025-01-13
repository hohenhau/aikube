resource "docker_image" "fastapi_app" {
  name = "localhost:5002/aikube-fastapi_app:latest"

  build {
    path = "../fastapi_app"  # Path to the FastAPI app Dockerfile
  }

  provisioner "local-exec" {
    command = "docker push localhost:5002/aikube-fastapi_app:latest"
  }
}

resource "docker_image" "ml_model" {
  name = "localhost:5002/aikube-ml_model:latest"

  build {
    path = "../ml_model"  # Path to the ML model Dockerfile
  }

  provisioner "local-exec" {
    command = "docker push localhost:5002/aikube-ml_model:latest"
  }
}
