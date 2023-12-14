variable "repository_names" {
  description = "List of docker image repository names"
  default = [
    "song-library",
    "singers"
  ]
}

resource "aws_ecr_repository" "image_repo" {
  for_each = toset(var.repository_names)

  name = "karaoke-image-${terraform.workspace}-${each.key}"
}

terraform {
  required_providers {

    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.58.0"
    }
  }

  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "spikes"

    workspaces {
      prefix = "karaoke-image-"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}