from PIL import Image
import collections
import io

def find_most_common_color(file):
    """Finds the most common color in an image file"""
    # Open the image file
    image = Image.open(file)

    # Get pixels from the image
    pixels = image.getdata()

    # Count the occurrences of each color
    color_counter = collections.Counter(pixels)

    # Find the most common color
    most_common_color = color_counter.most_common(1)[0][0]

    # Return the most common color
    return most_common_color


def most_common_color(image_file: io.BytesIO) -> str:
    """Finds the most common color in an image file"""
    return find_most_common_color(image_file)