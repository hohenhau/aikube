# Build and push FastAPI app
resource "null_resource" "build_and_push_fastapi_app" {
  triggers = {
    dockerfile_content = filemd5("../fastapi_app/Dockerfile")
    requirements_content = filemd5("../fastapi_app/requirements.txt")
    app_content = join("", [for f in fileset("../fastapi_app/app", "*.py") : filemd5("../fastapi_app/app/${f}")])
  }

  depends_on = [docker_container.local_registry]

  provisioner "local-exec" {
    command = <<-EOT
      # Wait for registry to be ready
      timeout=60
      counter=0
      echo "Waiting for registry to be available..."
      until curl -s http://localhost:5002/v2/ > /dev/null; do
        sleep 1
        counter=$((counter + 1))
        if [ $counter -ge $timeout ]; then
          echo "Registry timeout after $timeout seconds"
          exit 1
        fi
      done
      
      # Build and push FastAPI image
      docker build -t localhost:5002/aikube-fastapi_app:latest ../fastapi_app
      docker push localhost:5002/aikube-fastapi_app:latest
    EOT
  }
}

# Build and push ML model
resource "null_resource" "build_and_push_ml_model" {
  triggers = {
    dockerfile_content = filemd5("../ml_model/Dockerfile")
    requirements_content = filemd5("../ml_model/requirements.txt")
    model_content = filemd5("../ml_model/model.py")
  }

  depends_on = [docker_container.local_registry]

  provisioner "local-exec" {
    command = <<-EOT
      # Wait for registry to be ready
      timeout=60
      counter=0
      echo "Waiting for registry to be available..."
      until curl -s http://localhost:5002/v2/ > /dev/null; do
        sleep 1
        counter=$((counter + 1))
        if [ $counter -ge $timeout ]; then
          echo "Registry timeout after $timeout seconds"
          exit 1
        fi
      done

      # Build and push ML model image
      docker build -t localhost:5002/aikube-ml_model:latest ../ml_model
      docker push localhost:5002/aikube-ml_model:latest
    EOT
  }
}