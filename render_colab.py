"""Run the renderer into /content and report the resulting PNG."""

import hashlib
import os

import main

FOLDER = "/content"
PICTURE = os.path.join(FOLDER, "entry.png")


def main_wrapper():
    """Render once, then print image size and file digest."""
    main.render(FOLDER)
    with open(PICTURE, "rb") as handle:
        payload = handle.read()
    print("size:", len(payload), "bytes")
    print("sha256:", hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main_wrapper()
