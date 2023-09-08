# Runpod Serverless GGUF

Builds docker image for runpod serverless containers based on GGUF models from huggingface.

As of now, only supports models without split files (due to Huggingface limitation < 50GB).

## Usage

```bash
export DOCKER_BUILDKIT=1 # Important to activate buildkit
export MODEL=TheBloke/CodeLlama-34B-Instruct-GGUF # Repository name, make sure .gguf files are existend
export QUANTITIZATION=Q5_K_S # This must match the filename for the target quantitization, will download codellama-34b-instruct.Q5_K_S.gguf
export HF_TOKEN=your_hugging_face_token_here

docker build -t runpod-images:dev . --platform linux/amd64 --build-arg HUGGING_FACE_HUB_TOKEN=$HF_TOKEN --build-arg MODEL_NAME=$MODEL --build-arg QUANTITIZATION=$QUANTITIZATION
```
