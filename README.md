# Font Compare

This project aims to evaluate the readability of different fonts when 3D printed. The program will generate test SVG files for each font, process them through a slicer (e.g., PrusaSlicer), and compare the printed output to the original font to assess readability.

## Project Structure

```
font-compare/
├── README.md
├── src/
│   ├── font_to_svg.py         # Script to generate SVG test files for each font
│   ├── svg_to_gcode.py        # Script to convert SVG files to G-code using a slicer
│   ├── gcode_to_images.py     # Script to convert G-code files to images for visualization
│   ├── compare_output.py      # Script to compare the printed output to the original font
├── tests/
│   ├── test_font_to_svg.py    # Unit tests for font_to_svg.py
│   ├── test_svg_to_gcode.py   # Unit tests for svg_to_gcode.py
│   ├── test_gcode_to_images.py # Unit tests for gcode_to_images.py
│   ├── test_compare_output.py # Unit tests for compare_output.py
├── data/
│   ├── fonts/                 # Directory containing font files
│   ├── generated_svgs/        # Directory for generated SVG files
│   ├── gcode/                 # Directory for G-code files
│   ├── printed_results/       # Directory for scanned/photographed printed results
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore file
```

## Tasks

1. **Generate Test SVG Files**
   - Create a script (`font_to_svg.py`) to generate simple SVG test files for each font.
   - Save the generated files in the `data/generated_svgs/` directory.

2. **Convert SVG to G-code**
   - Create a script (`svg_to_gcode.py`) to pass the generated SVG files to a slicer (e.g., PrusaSlicer).
   - Save the resulting G-code files in the `data/gcode/` directory.

3. **Convert G-code to Images**
   - Create a script (`gcode_to_images.py`) to convert G-code files into images for visualization.
   - Save the resulting images in the `data/printed_results/` directory.

4. **Compare Printed Output**
   - Create a script (`compare_output.py`) to compare the printed output to the original font.
   - Use image processing techniques to assess readability.

5. **Testing**
   - Write unit tests for each script in the `tests/` directory.

6. **Documentation**
   - Document the process and usage of the program in the `README.md` file.

## Requirements

- Python 3.8+
- PrusaSlicer or another compatible slicer
- Image processing library (e.g., OpenCV)

## Getting Started

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd font-compare
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:

     ```bash
     # On macOS:
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   brew install cairo gobject-introspection
   pip install -r requirements.txt
   ```

5. Run the scripts as needed:
   - Generate test SVG files: `python src/font_to_svg.py`
   - Convert SVG to G-code: `python src/svg_to_gcode.py`
   - Convert G-code to images: `python src/gcode_to_images.py`
   - Compare output: `python src/compare_output.py`

6. To deactivate the virtual environment when done:

   ```bash
   deactivate
   ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## TODO

* [ ] Wingdings does not work with cairo/pango

## Thanks

- <https://aperiodic.net/pip/archives/Geekery/cairo-pango-python/>
