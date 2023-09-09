# Runpod Serverless GGUF

Builds docker image for runpod serverless containers based on GGUF models from huggingface.

As of now, only supports models without split files (due to Huggingface limitation < 50GB).

## Building

To build the easy way, use the python script and dynamically input the parameters:

```bash
$ python build.py
Enter MODEL (default: TheBloke/CodeLlama-34B-Instruct-GGUF):
Enter QUANTITIZATION (default: Q5_K_S):
Enter IS_70B (yes/no, default: no):
Enter HF_TOKEN:
Enter REPOSITORY_NAME (default: myuser/my-test-image):
Push Image to repository (yes/no, default: no):
Building Image: myuser/my-test-image:thebloke-codellama-34b-instruct-gguf-Q5_K_S-CUBLAS
```

Alternatively, build it yourself:

```bash
export DOCKER_BUILDKIT=1 # Important to activate buildkit
export MODEL=TheBloke/CodeLlama-34B-Instruct-GGUF # Repository name, make sure .gguf files are existend
export QUANTITIZATION=Q5_K_S # This must match the filename for the target quantitization, will download codellama-34b-instruct.Q5_K_S.gguf
export HF_TOKEN=your_hugging_face_token_here

docker build -t runpod-images:dev . --platform linux/amd64 --build-arg HUGGING_FACE_HUB_TOKEN=$HF_TOKEN --build-arg MODEL_NAME=$MODEL --build-arg QUANTITIZATION=$QUANTITIZATION
```

If model is a 70b parameter model, the following build arg must be added:

```bash
--build-arg IS_70B=True
```

## Testing Image

Create file `test_input.json` with input values for the model:

```json
{
  "input": {
    "prompt": "Q: What is Python?\nA:",
    "stop": ["Q:", "\n"],
    "max_tokens": 50
  }
}
```

To run the image with the input:

```bash
docker run -v $(pwd)/test_input.json:/test_input.json runpod-images:dev
```

## Usage

Following environment variables are available:

- `N_CTX`: Context Size
- `NUM_GPU_SHARD`: Number of GPU shards.

The POST Request input should have the structure of the `input` key in the test file:

```json
{
  "prompt": "Q: What is Python?\nA:",
  "stop": ["Q:", "\n"],
  "max_tokens": 50
}
```
