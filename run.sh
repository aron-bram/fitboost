#!/bin/bash

# Function to start a service in the background
start_service() {
  local service_name="$1"
  local dir="$2"
  local command="$3"
  cd $dir
  echo "Starting $service_name..."
  echo "Running: $command under $PWD"
  # Use nohup to detach the process from the terminal and & to run it in the background
  nohup $command &> "/tmp/$service_name.log" 2>&1 &
  disown # Detach the process from the current shell session
  cd -
}

# Start services using the defined function
start_service "ML Service" "." "python ml-service/src/ml-service/predictor_api.py"
start_service "Backend" "backend" "node server.js"
start_service "Frontend" "frontend/fitboost" "npx expo start"

echo "All services started in the background. Logs are available in /tmp directory."