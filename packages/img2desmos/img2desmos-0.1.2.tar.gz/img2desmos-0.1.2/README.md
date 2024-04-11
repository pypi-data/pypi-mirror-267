# Img2Desmos

This is a simple python script that converts an image to the bezier curves which can be plotted on desmos.

![image](https://github.com/Perchinka/img2desmos/assets/34923601/9579d060-ae62-4a45-bca7-415ef9858876)


## Requirements

- Python 3.11
- Poetry
- [Optional] Chafa (for previewing the images in terminal)

## Installation

```bash
pip install img2desmos
```

## Usage

```bash
> img2desmos --help
                                                                                             
 Usage: img2desmos [OPTIONS] IMG                                                             
                                                                                             
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────╮
│ *    img      TEXT  Path to the image to convert into graph [default: None] [required]    │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮
│ --output   -o      TEXT     Output formulas file path [default: None]                     │
│ --preview  -p               Preview the img in a window (chafa is required)               │
│ --upper            INTEGER  Upper threshold for the edge detection [default: 200]         │
│ --lower            INTEGER  Lower threshold for the edge detection [default: 100]         │
│ --help                      Show this message and exit.                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────╯

```
