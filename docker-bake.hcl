group "default" {
  targets = ["actions-runner"]
}

target "actions-runner" {
  context    = "actions-runner"
  dockerfile = "Dockerfile"
  tags = ["fengheai/actions-runner:latest"]
}

target "compass-runtime" {
  context    = "compass-runtime"
  dockerfile = "Dockerfile"
  tags = ["fengheai/compass-runtime"]
}

target "git-tools" {
  context    = "git-tools"
  dockerfile = "Dockerfile"
  tags = ["fengheai/git-tools:latest"]
}

target "github-token-manager" {
  context    = "github-token-manager"
  dockerfile = "Dockerfile"
  tags = ["fengheai/github-token-manager:latest"]
}

target "mlflow" {
  context    = "mlflow"
  dockerfile = "Dockerfile"
  tags = ["fengheai/mlflow:latest"]
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
