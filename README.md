# Python App for RunPod

This is a Python application designed to be deployed as a Docker container on RunPod.io.

## Project Structure

- `app.py` - Flask app that handles HTTP requests
- `runpod_handler.py` - Handler for RunPod serverless functions
- `Dockerfile` - Container definition
- `requirements.txt` - Python dependencies
- `environment.yml` - Conda environment configuration

## Local Development

### Using pip

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Test the RunPod handler:
   ```
   python runpod_handler.py
   ```

### Using Conda

1. Create and activate the conda environment:
   ```
   conda env create -f environment.yml
   conda activate runpod-app
   ```


3. Test the RunPod handler:
   ```
   python runpod_handler.py
   ```

## Building and Running Docker

```bash
# Build Docker image
docker build -t sschat/llm-frontend:main .

# Run container locally
docker run -p 8000:8000 sschat/llm-frontend:main
```

## Deploying to RunPod

1. Push your Docker image to a container registry (Docker Hub, GitHub Container Registry, etc.)
2. Create a new pod on RunPod.io using your container image
3. Configure the pod with appropriate resources for your workload

## API Endpoints

- `GET /healthcheck` - Health check endpoint
- `POST /api` - Main API endpoint for processing requests