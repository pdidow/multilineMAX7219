from PIL import Image
from dataclasses import dataclass
import os
import argparse
from typing import List

@dataclass
class Sprite:
    index: int
    pixels: List[List[int]]

def load_spritesheet(filename, sprite_size):
    sprites = []

    # Load the spritesheet into an image object
    spritesheet = Image.open(filename).convert("L")  # Convert to grayscale

    # Get the size of the spritesheet
    sheet_width, sheet_height = spritesheet.size
    
    print(f"Sheet width: {sheet_width}, Sheet Height: {sheet_height}")
    print(f"SpriteSize: {sprite_size}")

    # Calculate the number of sprites in the sheet
    num_sprites_x = sheet_width // sprite_size[0]
    num_sprites_y = sheet_height // sprite_size[1]

    # Create a folder for each sprite
    output_folder = "output_sprites"
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each row and column of sprites
    for row in range(num_sprites_y):
        for col in range(num_sprites_x):
            # Calculate the coordinates of the current sprite
            x = col * sprite_size[0]
            y = row * sprite_size[1]

            # Crop the sprite from the spritesheet
            sprite_image = spritesheet.crop((x, y, x + sprite_size[0], y + sprite_size[1]))

            # Convert the sprite image to a 2D array of pixel values
            sprite_pixels = [
                [1 if pixel > 127 else 0 for pixel in sprite_image.getdata()][i:i+sprite_size[0]]
                for i in range(0, len(sprite_image.getdata()), sprite_size[0])
            ][:sprite_size[1]]

            # Create a Sprite object and add it to the list
            sprite_index = row * num_sprites_x + col
            sprite = Sprite(index=sprite_index, pixels=sprite_pixels)

            # Save each sprite's array as a separate file
            output_filename = os.path.join(output_folder, f"sprite_{sprite.index}.txt")
            with open(output_filename, "w") as file:
                for i, sprite_row in enumerate(sprite.pixels):
                    file.write("[" + ", ".join(map(str, sprite_row)) + "]")
                    if i < len(sprite.pixels) - 1:
                        file.write(",")
                    file.write("\n")
            print(f"Sprite {sprite.index} saved to {output_filename}")

            sprites.append(sprite)

    return sprites

def main():
    parser = argparse.ArgumentParser(description="Process spritesheet and save individual sprites.")
    parser.add_argument("filename", help="Path to the spritesheet image file")
    parser.add_argument("spriteSize", type=int, nargs=2, help="Size of each sprite (width and height)")

    args = parser.parse_args()

    spritesheet_filename = args.filename
    sprite_size = list(args.spriteSize)  # Convert to list

    # Load sprites from the spritesheet
    sprites = load_spritesheet(spritesheet_filename, sprite_size)

if __name__ == "__main__":
    main()
