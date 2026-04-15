#!/usr/bin/env python3

import argparse
import sys

sys.path.append("/root/docksmith")

from builder import build
from runtime import run_image


def parse_env_variables(env_list):
    env_dict = {}

    if env_list:
        for item in env_list:
            if "=" in item:
                key, value = item.split("=", 1)
                env_dict[key] = value

    return env_dict


def main():
    parser = argparse.ArgumentParser(description="Docksmith CLI")

    parser.add_argument("command", choices=["build", "run"])
    parser.add_argument("tag", nargs="?")
    parser.add_argument("-t", "--tag-name")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("-e", "--env", action="append", help="Environment variables")

    args = parser.parse_args()

    if args.command == "build":
        image_tag = args.tag_name if args.tag_name else args.tag

        if not image_tag:
            print("Error: Please provide image tag")
            return

        build(image_tag, ".", args.no_cache)

    elif args.command == "run":
        image_tag = args.tag

        if not image_tag:
            print("Error: Please provide image tag")
            return

        env_vars = parse_env_variables(args.env)
        run_image(image_tag, env_vars)


if __name__ == "__main__":
    main()