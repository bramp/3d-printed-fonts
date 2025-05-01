#!/usr/bin/env python3
import os
import re
from PIL import Image, ImageDraw
from src.config import GCODE_DIR, OUTPUT_IMAGE_DIR

# Ensure output directories exist
os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)

def parse_gcode(file_path):
    """Parse G-code file and extract print moves."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    layers = []
    current_layer = []
    x, y = 0, 0

    for line in lines:
        if line.startswith(';LAYER:'):  # Detect layer change
            if current_layer:
                layers.append(current_layer)
                current_layer = []
        
        if line.startswith('G1') and 'X' in line and 'Y' in line:  # Detect print moves
            match_x = re.search(r'X([0-9\.]+)', line)
            match_y = re.search(r'Y([0-9\.]+)', line)
            if match_x and match_y:
                x = float(match_x.group(1))
                y = float(match_y.group(1))
                current_layer.append((x, y))

    if current_layer:  # Add the last layer
        layers.append(current_layer)

    return layers

def draw_layer(layer, width=200, height=200, scale=10):
    """Draw a single layer as an image."""
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    for i in range(1, len(layer)):
        x1, y1 = layer[i - 1]
        x2, y2 = layer[i]
        draw.line((x1 * scale, y1 * scale, x2 * scale, y2 * scale), fill='black', width=1)

    return image

def convert_gcode_to_images(gcode_file, output_dir):
    """Convert G-code file to images, one per layer."""
    layers = parse_gcode(gcode_file)
    base_name = os.path.splitext(os.path.basename(gcode_file))[0]

    for i, layer in enumerate(layers):
        image = draw_layer(layer)
        output_path = os.path.join(output_dir, f"{base_name}_layer_{i + 1}.png")
        image.save(output_path)
        print(f"Saved layer {i + 1} to {output_path}")

def main():
    """Main function to convert G-code files to images."""
    gcode_files = [os.path.join(GCODE_DIR, f) for f in os.listdir(GCODE_DIR) if f.endswith('.gcode')]

    if not gcode_files:
        print("No G-code files found in the directory.")
        return

    for gcode_file in gcode_files:
        convert_gcode_to_images(gcode_file, OUTPUT_IMAGE_DIR)

if __name__ == "__main__":
    main()