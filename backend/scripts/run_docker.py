#!/usr/bin/env python3
"""
Script to run Docker containers for the application
"""

import subprocess
import sys
import os

def run_docker_compose():
    """Run the application using Docker Compose"""
    try:
        # Change to the docker directory
        docker_dir = os.path.join(os.path.dirname(__file__), "..", "docker")
        os.chdir(docker_dir)
        
        # Run docker-compose up
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("Docker containers started successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running Docker Compose: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Docker Compose not found. Please install Docker and Docker Compose.")
        sys.exit(1)

def stop_docker_compose():
    """Stop the Docker containers"""
    try:
        docker_dir = os.path.join(os.path.dirname(__file__), "..", "docker")
        os.chdir(docker_dir)
        
        subprocess.run(["docker-compose", "down"], check=True)
        print("Docker containers stopped successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Docker Compose: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        stop_docker_compose()
    else:
        run_docker_compose() 