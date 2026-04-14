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