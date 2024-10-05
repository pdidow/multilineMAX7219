import time
from multilineMAX7219 import MultilineMax7219  # Updated import name

def main():
    # Initialize the library and the MAX7219/8x8LED arrays
    MultilineMax7219.init()  # Updated initialization

    print("Do not forget to update MATRIX_WIDTH and MATRIX_HEIGHT in multilineMAX7219.py prior to this test")

    try:
        # Clear all LEDs on the matrix
        MultilineMax7219.clear_all()  # Updated method call

        # Set the brightness to 0 (minimum brightness)
        MultilineMax7219.brightness(0)  # Updated method call

        # Define the heart symbol as a pixel map
        heart = [
            [0, 1, 0, 0, 0, 0, 1, 0],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # Connect to the MAX7219 display
        display = MultilineMax7219(1, 8, 8)

        # Display the heart symbol
        for row in range(8):
            for col in range(8):
                display.pixel(row, col, heart[row][col])

        # Update the display
        display.show()

        # Keep the display on for a few seconds
        time.sleep(5)

        # Clear the display
        display.clear()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
