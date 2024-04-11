#!/usr/bin/env python

import os
from sympy import symbols, latex
from svg.path import parse_path
from xml.dom.minidom import parse

import typer
import pyperclip
from rich.progress import Progress, SpinnerColumn, TextColumn

import cv2
import subprocess

from termcolor import colored

import potrace
import numpy as np
from PIL import Image


def png_to_svg(png_file: str, svg_file: str, upper_threshold: int = 0, lower_threshold: int = 100):
    # Edge detection
    img = cv2.imread(png_file, 0)
    edges = cv2.Canny(img, lower_threshold, upper_threshold)

    pnm_file = '/tmp/output.pnm'
    cv2.imwrite(pnm_file, edges)

    try:
        image = Image.open(pnm_file)
    except IOError:
        raise Exception("Error opening the image")

    bm = potrace.Bitmap(image, blacklevel=0.5)
    paths = bm.trace(
        turdsize=2,
        turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
        alphamax=1,
        opticurve=False,
        opttolerance=0.2
        )      
    with open(svg_file, "w") as fp:
        fp.write(
            f'''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{image.width}" height="{image.height}" viewBox="0 0 {image.width} {image.height}">''')
        parts = []
        for curve in paths:
            fs = curve.start_point
            parts.append(f"M{fs.x},{fs.y}")
            for segment in curve.segments:
                if segment.is_corner:
                    a = segment.c
                    b = segment.end_point
                    parts.append(f"L{a.x},{a.y}L{b.x},{b.y}")
                else:
                    a = segment.c1
                    b = segment.c2
                    c = segment.end_point
                    parts.append(f"C{a.x},{a.y} {b.x},{b.y} {c.x},{c.y}")
            parts.append("z")
        fp.write(f'<path stroke="none" fill="black" fill-rule="evenodd" d="{"".join(parts)}"/>')
        fp.write("</svg>") 

    os.remove(pnm_file)

def print_bezier_formula(svg_file: str):
    dom = parse(svg_file)
    paths = dom.getElementsByTagName('path')

    for path in paths:
        path_data = path.getAttribute('d')
        path = parse_path(path_data)
        result = []
        for segment in path:
            if segment.__class__.__name__ == 'CubicBezier':
                t = symbols('t')
                s = symbols('s')
                N_x = s * ((1-t)**3*segment.start.real + 3*(1-t)**2*t*segment.control1.real + 3*(1-t)*t**2*segment.control2.real + t**3*segment.end.real)
                N_y = s * ((1-t)**3*segment.start.imag + 3*(1-t)**2*t*segment.control1.imag + 3*(1-t)*t**2*segment.control2.imag + t**3*segment.end.imag)
                result.append(f"({latex(N_x)},{latex(N_y)})")
        
        result.append('s = 0.01')
        return result
    

def main(
        img: str = typer.Argument(..., help='Path to the image to convert into graph'),
        formulas_path: str = typer.Option(None, '-o', '--output', help='Output formulas file path'),
        preview: bool = typer.Option(False, '-p', '--preview', help='Preview the img in a window (chafa is required)'), 
        upper_threshold: int = typer.Option(200, '--upper', help='Upper threshold for the edge detection'),
        lower_threshold: int = typer.Option(100, '--lower', help='Lower threshold for the edge detection'),     
):
    svg_path = '/tmp/output.svg'

    png_to_svg(img, svg_path, upper_threshold, lower_threshold)
    if preview:
        subprocess.run(f'chafa {img} {svg_path}', shell=True)
        
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Calculating Formulas...", total=None)
        formulas_string = '\n'.join(print_bezier_formula(svg_path))
    print(f" - {colored('Calculations done', 'green')}")

    pyperclip.copy(formulas_string)
    print(f" - {colored('Formulas copied to the clipboard', 'green')}")

    if formulas_path:
        with open(formulas_path, 'w') as f:
            f.write(formulas_string)
            print(f" - {colored('Formulas saved in', 'green')} {colored(os.path.abspath(formulas_path), 'yellow')}")

def start():
    typer.run(main)

if __name__ == "__main__":
    start()
