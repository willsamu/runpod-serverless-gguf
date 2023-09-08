import runpod
import os
import time
import json
from llama_cpp import Llama

# Prepare the model and tokenizer
MODEL_NAME = os.environ.get('MODEL_NAME')
MODEL_BASE_PATH = os.environ.get('MODEL_BASE_PATH', '/runpod-volume/')
STREAMING = os.environ.get('STREAMING', False) == 'True'
TOKENIZER = os.environ.get('TOKENIZER', None)
USE_FULL_METRICS = os.environ.get('USE_FULL_METRICS', True)

# ? Optional Parameters which are set via environment
IS_70B = os.environ.get('IS_70B', False) == 'True'

# ? Optional Parameters which are set via environment
n_ctx = 1500
try:
    n_ctx = int(os.environ.get('N_CTX'))
except Exception as e:
    print("N_CTX must be given and an integer")
    

if not MODEL_NAME:
    print("Error: The model has not been provided.")

# Tensor parallelism
try:
    NUM_GPU_SHARD = int(os.environ.get('NUM_GPU_SHARD', 1))
except Exception as e:
    print("Error: NUM_GPU_SHARD should be existend and an integer. Using default value of 1.")
    NUM_GPU_SHARD = 1

# ? Get Model file - curretnly only supports exactly one file
model_file = f"{MODEL_BASE_PATH}{MODEL_NAME.split('/')[1]}"
# List all files in the directory
files = [f for f in os.listdir(model_file) if os.path.isfile(os.path.join(model_file, f))]
# Check if there's exactly one file in the directory
if len(files) == 1:
    model_file = os.path.join(model_file, files[0])
else:
    print("There's either no file or more than one file in the directory: ", model_file, files)

# ? Required to load 70 Models. See: https://github.com/abetlen/llama-cpp-python#loading-llama-2-70b
loading_kwargs = {}
if IS_70B:
    loading_kwargs["n_gqa"] = 8

loading_kwargs["n_ctx"] = n_ctx

llm = Llama(
        model_path=model_file, 
        n_gpu_layers=NUM_GPU_SHARD, # Offload all layers to GPU
        **loading_kwargs
        )

## load your model(s) into vram here

def handler(event):
    print("Job received by handler: {}".format(event))
    input = event['input']

    # ? Parse Inputs
    max_tokens = input.get('max_tokens', 200)
    stop = input.get('stop', ["Q:", "\n"])
    prompt = input.get('prompt', None)

    if prompt is None:
        return {
            "error": "Prompt is required."
        }

    # ? Generate Response
    output = llm(prompt, max_tokens=max_tokens, stop=stop, echo=True)
    
    print(output)
    result = output["choices"][0]["text"]
    usage = {
            "prompt_tokens": output["usage"]["prompt_tokens"],
            "completion_tokens": output["usage"]["completion_tokens"],
            "total_tokens": output["usage"]["total_tokens"],
    }

    return json.dumps({
        "result": result, 
        "usage": usage
    })

runpod.serverless.start({
    "handler": handler
})