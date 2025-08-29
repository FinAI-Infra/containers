group "default" {
  targets = ["runpod_260", "runpod_280"]
}

target "github-token-manager" {
  context    = "github-token-manager"
  dockerfile = "Dockerfile"
  tags = ["fengheai/github-token-manager:latest"]
}

target "runpod_260" {
  context    = "runpod"
  dockerfile = "Dockerfile"
  args = {
    PYTORCH_VERSION = "2.6.0"
  }
  tags = ["fengheai/runpod:2.6.0"]
}

target "runpod_280" {
  context    = "runpod"
  dockerfile = "Dockerfile"
  args = {
    PYTORCH_VERSION = "2.8.0"
  }
  tags = ["fengheai/runpod:2.8.0"]
}
