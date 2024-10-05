# filename: led_matrix_utils.py

from PIL import Image
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop

def convert_to_binary_image(image_data, threshold=128):
    binary_image = []
    for pixel in image_data:
        grayscale = (pixel[0] + pixel[1] + pixel[2]) / 3
        binary_value = 1 if grayscale >= threshold else 0
        binary_image.append(binary_value)
    return binary_image

def display_image_on_led_matrix(image_path, threshold=128):
    # Load PNG image
    image = Image.open(image_path)

    # Convert image to a list of pixels
    image_data = list(image.getdata())

    # Call the conversion function
    matrix_data = convert_to_binary_image(image_data, threshold)

    # Set up MAX7219 display
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=3, block_orientation=-90, rotate=0)

    # Iterate through the LED matrix data and update the display
    for i in range(device.width * device.height):
        device.pixel(i % device.width, i // device.width, matrix_data[i])

    # Display the result
    input("Press Enter to exit...")

if __name__ == "__main__":
    # Example usage
    display_image_on_led_matrix("path/to/your/image.png")
#This way, you can import the module and use both functions in a cohesive manner:
#python

#from led_matrix_utils import convert_to_binary_image, display_image_on_led_matrix

# Use the functions as needed
#image_path = "path/to/your/image.png"
#image_data = [...]  # Your pixel data
#binary_image = convert_to_binary_image(image_data)
#display_image_on_led_matrix(image_path)
