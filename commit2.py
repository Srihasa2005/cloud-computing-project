import os
import shutil
import json
import time
import tempfile
import subprocess
from utils import *

DOCK_DIR = os.path.expanduser("~/.docksmith")

def parse_file(path):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]

def build(tag, context, no_cache=False):
    lines = parse_file(os.path.join(context, "Docksmithfile"))

    temp_dir = os.path.join(tempfile.gettempdir(), "docksmith_build")

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(f"{DOCK_DIR}/layers", exist_ok=True)

    layers = []
    prev_digest = ""
    env = {}
    workdir = "/"
    cmd = ""

    for step, line in enumerate(lines, start=1):
        parts = line.split(" ", 1)
        instr = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        print(f"Step {step}: {line}")

        if instr == "FROM":
            prev_digest = "base"

        elif instr == "WORKDIR":
            workdir = arg
            os.makedirs(temp_dir + workdir, exist_ok=True)

        elif instr == "ENV":
            k, v = arg.split("=")
            env[k] = v

        elif instr == "COPY":
            src, dest = arg.split()

            source_path = os.path.expanduser(src)
            source_path = source_path if os.path.isabs(source_path) else os.path.join(context, source_path)

            dest_path = temp_dir + dest

            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Source path not found: {source_path}")

            if os.path.isdir(source_path):
                shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(source_path, dest_path)

            # 🔥 create layer after COPY
            tar_path = os.path.join(tempfile.gettempdir(), "layer.tar")
            if os.path.exists(tar_path):
                os.remove(tar_path)

            create_tar(temp_dir, tar_path)

            layer_digest = sha256_file(tar_path)
            shutil.move(tar_path, f"{DOCK_DIR}/layers/{layer_digest}.tar")

            layers.append(layer_digest)
            prev_digest = layer_digest

        elif instr == "RUN":
            run_cmd = arg

            if run_cmd.startswith("/bin/echo"):
                run_cmd = run_cmd.replace("/bin/echo", "echo")

            subprocess.run(run_cmd, shell=True, check=True)

            # 🔥 create layer after RUN
            tar_path = os.path.join(tempfile.gettempdir(), "layer.tar")
            if os.path.exists(tar_path):
                os.remove(tar_path)

            create_tar(temp_dir, tar_path)

            layer_digest = sha256_file(tar_path)
            shutil.move(tar_path, f"{DOCK_DIR}/layers/{layer_digest}.tar")

            layers.append(layer_digest)
            prev_digest = layer_digest

        elif instr == "CMD":
            cmd = arg