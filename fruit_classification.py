from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def load_image(image_path):
    """Load an image and convert it to RGB."""
    image = Image.open(image_path).convert("RGB")
    return np.array(image)


def show_image(image):
    """Display an image."""
    plt.imshow(image)
    plt.axis("off")
    plt.show()


def extract_features(image):
    """Extract simple average color features."""
    image = image.astype(np.float32) / 255.0

    mean_rgb = image.mean(axis=(0, 1))

    return {
        "mean_red": round(float(mean_rgb[0]), 3),
        "mean_green": round(float(mean_rgb[1]), 3),
        "mean_blue": round(float(mean_rgb[2]), 3),
    }


def main():
    image_path = input("Enter the image file path: ").strip()

    if not Path(image_path).is_file():
        print("Image file not found.")
        return

    image = load_image(image_path)
    features = extract_features(image)

    show_image(image)

    print("Extracted image features:")
    for name, value in features.items():
        print(f"{name}: {value}")

    print(
        "\nThis is a preliminary image-processing step. "
        "A trained model and labeled fruit images are needed "
        "for actual fruit classification."
    )


if __name__ == "__main__":
    main()
