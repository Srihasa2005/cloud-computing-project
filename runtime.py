import os
import shutil
import json
import tempfile

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

    print("Running container...")