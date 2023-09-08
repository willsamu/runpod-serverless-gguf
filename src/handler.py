import runpod
import os
import time
from llama_cpp import Llama

llm = Llama(model_path="./models/7B/ggml-model.bin")

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