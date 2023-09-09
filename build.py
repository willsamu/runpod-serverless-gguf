import os
import subprocess

# Get user inputs
os.environ["DOCKER_BUILDKIT"] = "1"
MODEL = input("Enter MODEL (default: TheBloke/CodeLlama-34B-Instruct-GGUF): ") or "TheBloke/CodeLlama-34B-Instruct-GGUF"
QUANTITIZATION = input("Enter QUANTITIZATION (default: Q5_K_S): ") or "Q5_K_S"
IS_70B_input = input("Enter IS_70B (yes/no, default: no): ").lower() or "no"
IS_70B = "True" if IS_70B_input == "yes" else "False"
HF_TOKEN = input("Enter HF_TOKEN:")
REPOSITORY_NAME = input("Enter REPOSITORY_NAME (default: myuser/my-test-image): ") or "myuser/my-test-image"

# Build IMAGE_NAME
model_user = MODEL.split('/')[0].replace("-", "").lower()
model_name = MODEL.split('/')[1].lower()
IMAGE_NAME = f"{REPOSITORY_NAME}:{model_user}-{model_name}-{QUANTITIZATION}-CUBLAS"
print(f"Building Image: {IMAGE_NAME}")


# Invoke Docker command
cmd = f"DOCKER_BUILDKIT=1 docker build -t {IMAGE_NAME} . --platform linux/amd64 --build-arg HUGGING_FACE_HUB_TOKEN={HF_TOKEN} --build-arg MODEL_NAME={MODEL} --build-arg QUANTITIZATION={QUANTITIZATION} --build-arg IS_70B={IS_70B}"
subprocess.run(cmd, shell=True)
