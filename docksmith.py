#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import sys

sys.path.append("/root/docksmith")

from builder import build
from runtime import run_image

IMAGES_DIR = "/root/.docksmith/images"


def parse_env_variables(env_list):
    env_dict = {}

    if env_list:
        for item in env_list:
            if "=" in item:
                key, value = item.split("=", 1)
                env_dict[key] = value

    return env_dict


def list_images():
    if not os.path.exists(IMAGES_DIR):
        print("No images found")
        return

    images = os.listdir(IMAGES_DIR)

    if not images:
        print("No images found")
        return

    print("Available Images:")
    for image in images:
        print(f"- {image}")


def remove_image(image_name):
    image_path = os.path.join(IMAGES_DIR, image_name)

    if not os.path.exists(image_path):
        print(f"Image '{image_name}' not found")
        return

    shutil.rmtree(image_path)
    print(f"Removed image '{image_name}'")


def main():
    parser = argparse.ArgumentParser(description="Docksmith CLI")

    parser.add_argument(
        "command",
        choices=["build", "run", "images", "rmi"]
    )

    parser.add_argument("tag", nargs="?")
    parser.add_argument("-t", "--tag-name")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("-e", "--env", action="append", help="Environment variables")

    main()