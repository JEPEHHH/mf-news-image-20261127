# World Dispatch - 27 November 2026

One deterministic 1024x1024 news broadsheet for the make.fun
`news-image-20261127` contest. The image sums up eleven stories from
Friday 27 November 2026: one lead, six illustrated features and four briefs.

## Run

Python 3 with Pillow and the DejaVu fonts is all that is needed. No network,
no install step, no clock and no randomness.

    mkdir -p out
    MAKEFUN_OUTPUT_DIR=out python3 main.py

The program writes `entry.png` into the chosen folder (`/output` by default)
and prints its path, dimensions and sha256 on stdout.

`render_colab.py` is a thin wrapper that calls `main.render("/content")`
and prints the size and sha256 of the resulting file.

## Files

- `main.py` - layout, copy, illustrations and entrypoint
- `render_colab.py` - Colab-friendly wrapper
- `LICENSE` - MIT, 2026 jepehhh
- `README.md` - this file

Licensed under MIT. The image is original work drawn entirely from code.
