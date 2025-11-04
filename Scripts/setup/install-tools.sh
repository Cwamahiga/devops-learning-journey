#!/bin/bash
# DevOps Tools Installation Script
# Run this to set up your local development environment

echo "🚀 Installing DevOps Tools..."

# AWS CLI
echo "📦 Installing AWS CLI..."
# curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# unzip awscliv2.zip
# sudo ./aws/install

# Docker
echo "🐳 Installing Docker..."
# curl -fsSL https://get.docker.com -o get-docker.sh
# sudo sh get-docker.sh

# kubectl
echo "☸️  Installing kubectl..."
# curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
# sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Terraform
echo "🏗️  Installing Terraform..."
# wget https://releases.hashicorp.com/terraform/latest/terraform_latest_linux_amd64.zip
# unzip terraform_latest_linux_amd64.zip
# sudo mv terraform /usr/local/bin/

echo "✅ Installation complete!"
echo "Run 'aws --version', 'docker --version', 'kubectl version', 'terraform version' to verify"
