import os
import shutil
import json
import tempfile
import subprocess
from utils import extract_tar

DOCK_DIR = os.path.expanduser("~/.docksmith")

def run_image(tag, env_override):
    name, image_tag = tag.split(":")
    image_path = f"{DOCK_DIR}/images/{name}_{image_tag}.json"

    with open(image_path) as f:
        data = json.load(f)

    temp_dir = os.path.join(tempfile.gettempdir(), "docksmith_run")

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.makedirs(temp_dir, exist_ok=True)

    # Extract layers
    for layer in data["layers"]:
        digest = layer["digest"].replace("sha256:", "")
        layer_path = f"{DOCK_DIR}/layers/{digest}.tar"

        if os.path.exists(layer_path):
            extract_tar(layer_path, temp_dir)

    # Working directory
    workdir = data["config"].get("WorkingDir", "/")
    full_workdir = os.path.join(temp_dir, workdir.lstrip("/"))

    os.makedirs(full_workdir, exist_ok=True)

    print("Running container...")

    # Execute command
    cmd = eval(data["config"]["Cmd"])

    subprocess.run(
        cmd,
        cwd=full_workdir,
        check=True
    )