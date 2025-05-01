#!/usr/bin/env python3
import os
from pathlib import Path
import cv2
from src.config import PRINTED_RESULTS_DIR, FONTS_DIR

# Ensure directories exist
os.makedirs(PRINTED_RESULTS_DIR, exist_ok=True)

def load_image(image_path: str):
    """Load an image from the given path."""
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def compare_images(original_image, printed_image):
    """Compare two images and return a similarity score."""
    # Resize printed image to match the original image size
    printed_image_resized = cv2.resize(printed_image, (original_image.shape[1], original_image.shape[0]))

    # Compute Structural Similarity Index (SSIM)
    score, _ = cv2.quality.QualitySSIM_compute(original_image, printed_image_resized)
    return score[0]

def main():
    """Main function to compare printed outputs to original fonts."""
    printed_files = [f for f in os.listdir(PRINTED_RESULTS_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not printed_files:
        print("No printed results found in the directory.")
        return

    for printed_file in printed_files:
        printed_path = os.path.join(PRINTED_RESULTS_DIR, printed_file)
        font_name = Path(printed_file).stem
        original_font_path = os.path.join(FONTS_DIR, f"{font_name}.png")  # Assuming original font images are saved as PNG

        if not os.path.exists(original_font_path):
            print(f"Original font image not found for {font_name}.")
            continue

        original_image = load_image(original_font_path)
        printed_image = load_image(printed_path)

        similarity_score = compare_images(original_image, printed_image)
        print(f"Similarity score for {font_name}: {similarity_score:.2f}")

if __name__ == "__main__":
    main()