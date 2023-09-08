#!pip install langchain

# model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
# model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin" # the model is in bin format

# from huggingface_hub import hf_hub_download, snapshot_download
# #model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)
# snapshot_download(repo_id=model_name_or_path, allow_patterns="*.json")

import os
from huggingface_hub import snapshot_download

# Get the hugging face token
HUGGING_FACE_HUB_TOKEN = os.environ.get('HUGGING_FACE_HUB_TOKEN', None)
MODEL_NAME = os.environ.get('MODEL_NAME')
MODEL_REVISION = os.environ.get('MODEL_REVISION', "main")
MODEL_BASE_PATH = os.environ.get('MODEL_BASE_PATH', '/runpod-volume/')
QUANTITIZATION = os.environ.get('QUANTITIZATION', False)
# Download the model from hugging face
download_kwargs = {}

if HUGGING_FACE_HUB_TOKEN:
    download_kwargs["token"] = HUGGING_FACE_HUB_TOKEN

snapshot_download(
    repo_id=MODEL_NAME,
    revision=MODEL_REVISION,
    local_dir=f"{MODEL_BASE_PATH}{MODEL_NAME.split('/')[1]}",
    allow_patterns=f"*{QUANTITIZATION}*" if QUANTITIZATION else "*", # ? If quantitization is true, then only download the quantitization model weights
    **download_kwargs
)

# # GPU Inference
# from llama_cpp import Llama
# lcpp_llm = None
# lcpp_llm = Llama(
#     model_path=model_path,
#     n_threads=2, # CPU cores
#     n_batch=512, # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
#     n_gpu_layers=32, # Change this value based on your model and your GPU VRAM pool.
#     n_ctx=1500
#     )