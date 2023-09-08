import runpod
import os
import time
from llama_cpp import Llama

# Prepare the model and tokenizer
MODEL_NAME = os.environ.get('MODEL_NAME')
MODEL_BASE_PATH = os.environ.get('MODEL_BASE_PATH', '/runpod-volume/')
STREAMING = os.environ.get('STREAMING', False) == 'True'
TOKENIZER = os.environ.get('TOKENIZER', None)
USE_FULL_METRICS = os.environ.get('USE_FULL_METRICS', True)

if not MODEL_NAME:
    print("Error: The model has not been provided.")

# Tensor parallelism
try:
    NUM_GPU_SHARD = int(os.environ.get('NUM_GPU_SHARD', 1))
except ValueError:
    print("Error: NUM_GPU_SHARD should be an integer. Using default value of 1.")
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

llm = Llama(
        model_path=model_file, 
        n_gpu_layers=1, # Offload all layers to GPU
        )

## load your model(s) into vram here

def handler(event):
    print(event)
    # do the things
    output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)
    print(output)
    

    return "Hello World"


runpod.serverless.start({
    "handler": handler
})