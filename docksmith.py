#!/usr/bin/env python3

import argparse
import sys

sys.path.append("/root/docksmith")

from builder import build
from runtime import run_image


def main():
    parser = argparse.ArgumentParser(description="Docksmith CLI")

    parser.add_argument("command", choices=["build", "run"])
    parser.add_argument("tag", nargs="?")
    parser.add_argument("-t", "--tag-name")
    parser.add_argument("--no-cache", action="store_true")

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

        run_image(image_tag, {})


if __name__ == "__main__":
    main()