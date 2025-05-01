#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import argparse
import xml.etree.ElementTree as ET
from config import SLICER_PATH, SVG_DIR, SIMPLIFIED_SVG_DIR, GCODE_DIR

ET.register_namespace("", "http://www.w3.org/2000/svg")

# Do this until https://github.com/prusa3d/PrusaSlicer/issues/14508 is fixed.
def simplify_svg(svg_file: str, output_file: str):
    """Simplify an SVG file by replacing <use> tags."""
    tree = ET.parse(svg_file)
    root = tree.getroot()

    parent_map = dict((c, p) for p in tree.iter() for c in p)

    # Replace <use> tags with their referenced content
    for use in root.findall(".//{http://www.w3.org/2000/svg}use"):
        parent = parent_map[use]

        href = use.attrib.get("{http://www.w3.org/1999/xlink}href")
        if href and href.startswith("#"):
            ref_id = href[1:]
            referenced = root.find(f".//*[@id='{ref_id}']")
            
            index = list(parent).index(use)
            
            if referenced is None:
                print(f"Warning: No definition found for {ref_id} in {svg_file}. Skipping <use> tag.")
            else:
                # Clone the referenced element and replace the <use> tag in place
                new_element = ET.Element(referenced.tag, referenced.attrib)
                new_element.text = referenced.text
                new_element.extend(referenced)
                new_element.tail = "\n" if referenced.tail is None else referenced.tail
                
                # Don't need the id attribute in the new element
                del new_element.attrib['id']

                x, y = float(use.attrib.get('x', '0')), float(use.attrib.get('y', '0'))
                if x > 0 or y > 0:
                    new_element.attrib['transform'] = f"translate({x} {y})"

                parent.insert(index, new_element)

            c = ET.Comment(f"<use id={href}/>")
            parent.insert(index, c)
            parent.remove(use)

    # Write the simplified SVG to the output file
    tree.write(output_file, xml_declaration=True, encoding='utf-8')
    print(f"Simplified SVG saved to {output_file}")



def convert_svg_to_gcode(svg_file: str, output_gcode: str, slicer_path: str):
    """Convert an SVG file to G-code using PrusaSlicer."""
    try:
        nozzle = 0.4  # Set nozzle diameter to 0.4mm
        layer_height = 0.2  # Set layer height to 0.2mm
        
        subprocess.run([
            slicer_path,
            "--export-gcode",

            # Try and ensure the first layer is pretty standard
            "--elefant-foot-compensation", "0",        # No elephant foot compensation
            #"--first-layer-extrusion-width", "100%",   # First layer extrusion width
            "--first-layer-height", str(layer_height), # First layer height

            "--layer-height", str(layer_height),  # All other layers are the same height
            # "--cut", str(layer_height),           # One layer height
            # "--scale-to-fit", "100, 100, 0.9",    # Fit the model within this volume
            "--output", output_gcode,

            # When we pass a SVG file, PrusaSlicer create a model with this code:
            # https://github.com/prusa3d/PrusaSlicer/blob/master/src/libslic3r/Format/SVG.cpp#L55 
            svg_file
        ], check=True)
        print(f"Converted {svg_file} to {output_gcode}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {svg_file} to G-code: {e}")


def main():
    """Main function to convert SVG files to G-code."""
    parser = argparse.ArgumentParser(description="Convert SVG files to G-code using PrusaSlicer.")
    parser.add_argument("svgs", nargs="*", help="Specific SVG files to process. If none are provided, all SVGs in the input directory will be processed.")
    args = parser.parse_args()

    if not os.path.exists(SLICER_PATH):
        print(f"Slicer not found at {SLICER_PATH}. Please update the path.")
        return

    if args.svgs:
        svg_files = args.svgs
    else:
        svg_files = [os.path.join(SVG_DIR, f) for f in os.listdir(SVG_DIR) if f.endswith('.svg')]

    if not svg_files:
        print("No SVG files found to process.")
        return

    # Ensure output directories exist
    os.makedirs(GCODE_DIR, exist_ok=True)
    os.makedirs(SIMPLIFIED_SVG_DIR, exist_ok=True)

    for svg_file in svg_files:
        if not os.path.exists(svg_file):
            print(f"SVG file not found: {svg_file}")
            continue

        # TODO In future skip this, if we detect the SVG is simple enough already
        try:
            simplified_svg = os.path.join(SIMPLIFIED_SVG_DIR, f"{Path(svg_file).stem}_simplified.svg")
            simplify_svg(svg_file, simplified_svg)
        except Exception as e:
            print(f"Error simplifying SVG {svg_file}: {e}")
            continue

        output_file = os.path.join(GCODE_DIR, f"{Path(svg_file).stem}.gcode")
        convert_svg_to_gcode(simplified_svg, output_file, SLICER_PATH)


if __name__ == "__main__":
    main()