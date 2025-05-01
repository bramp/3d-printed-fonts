#!/usr/bin/env python3
import os
import argparse
import cairo
import gi
from config import SVG_DIR

gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo  # noqa: E402

def print_font_tree():
    """Print the font families and their faces in a tree-like structure."""
    font_map = PangoCairo.font_map_get_default()
    families = font_map.list_families()

    print("System font families and their faces:")
    for family in sorted(families, key=lambda f: f.get_name()):
        family_name = family.get_name()
        faces = family.list_faces()
        print(f"- {family_name}")
        for face in faces:
            print(f"  - {face.get_face_name()}")

def generate_svg_from_font_family(font_family: str, output_file: str):
    """Generate a simple SVG sample file for a given font family using Pango and Cairo."""

    print("Generating SVG sample for font family: ", font_family)

    # Create an SVG surface and context
    surface = cairo.SVGSurface(output_file, 500, 200)
    try:
        context = cairo.Context(surface)

        # Create a Pango layout
        layout = PangoCairo.create_layout(context)
        layout.set_text("Test", -1)

        # Set the font description
        font_map = PangoCairo.font_map_get_default()
        font_family_obj = font_map.get_family(font_family)
        if not font_family_obj:
            print(f"Font family '{font_family}' not found. Skipping.")
            return

        # Pick the "Regular" face if available, otherwise use the first face
        faces = font_family_obj.list_faces()
        font_face = next((face for face in faces if face.get_face_name() == "Regular"), faces[0])
        font_desc = font_face.describe()
        font_desc.set_size(100 * Pango.SCALE)

        layout.set_font_description(font_desc)
        layout.set_alignment(Pango.Alignment.CENTER)

        # Get text extents to center the text
        ink_rect, logical_rect = layout.get_extents()
        text_width = logical_rect.width / Pango.SCALE
        text_height = logical_rect.height / Pango.SCALE

        x = (500 - text_width) / 2
        y = (200 - text_height) / 2

        # Move the layout to the centered position
        context.translate(x, y)

        # Draw a rectangular border around the text
        context.rectangle(-10, -10, text_width + 20, text_height + 20)  # Add padding around the text
        context.set_source_rgb(0, 0, 0)  # Black border
        context.set_line_width(2)
        context.stroke()

        # Render the text
        context.set_source_rgb(0, 0, 0)  # Black text
        PangoCairo.show_layout(context, layout)

        print(f"Generated test file for {font_desc.to_string()}: {output_file}")
    finally:
        # Ensure the surface is always finalized
        surface.finish()

def main():
    """Main function to generate test files for all system fonts."""
    parser = argparse.ArgumentParser(description="Generate test files for system fonts.")
    parser.add_argument("--list", action="store_true", help="List all system font families and exit.")
    parser.add_argument("fonts", nargs="*", help="Specific font family names to generate test files for.")
    args = parser.parse_args()

    if args.list:
        print_font_tree()
        return

    fonts = args.fonts or []
    if not fonts:
        print("No font families provided.")
        return

    # Ensure output directory exists
    os.makedirs(SVG_DIR, exist_ok=True)

    for font_family in fonts:
        output_file = os.path.join(SVG_DIR, f"{font_family}.svg")
        generate_svg_from_font_family(font_family, output_file)

if __name__ == "__main__":
    main()