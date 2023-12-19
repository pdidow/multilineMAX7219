# Sprite Extractor Utility

## Usage

Extract individual frames from a spritesheet and prepare them for animation with the playAni.py utility.

### Command
```bash
python3 spriteExtractor.py [spritesheetname.png] width height
Example

bash

python3 spriteExtractor.py sprites.png 8 8

    spritesheetname.png: The name of the source spritesheet file.
    width and height: The dimensions of each frame to be extracted from the source file.

Output

The extracted frames are placed in the output directory under the parent SpriteTool directory.
Animation Setup

    Copy the contents of the output directory.
    Create a new directory under the animationDemos folder.
    Paste the copied frames into the new directory.

Play Animation

Use the playAni.py animation playing utility to display the extracted frames.
Example

bash

python3 playAni.py [your_new_directory]

Replace [your_new_directory] with the name of the directory you created for your extracted frames.
Notes

    Ensure the spritesheet and the utility script are in the same directory or provide the correct file path.
    Adjust the width and height parameters based on your desired frame size.

vbnet


This version provides more structure, clarifies each section, and includes explicit instructions for the user. Feel free to adjust it further based on your preferences or additional details about your utility.

User
write all this out again in one thing so i can copy it
ChatGPT

Certainly! Here's the consolidated version for your readme:

markdown

# Sprite Extractor Utility

## Usage

Extract individual frames from a spritesheet and prepare them for animation with the playAni.py utility.

### Command
```bash
python3 spriteExtractor.py [spritesheetname.png] width height

Example

bash

python3 spriteExtractor.py sprites.png 8 8

    spritesheetname.png: The name of the source spritesheet file.
    width and height: The dimensions of each frame to be extracted from the source file.

Output

The extracted frames are placed in the output directory under the parent SpriteTool directory.
Animation Setup

    Copy the contents of the output directory.
    Create a new directory under the animationDemos folder.
    Paste the copied frames into the new directory.

Play Animation

Use the playAni.py animation playing utility to display the extracted frames.
Example

bash

python3 playAni.py [your_new_directory]

Replace [your_new_directory] with the name of the directory you created for your extracted frames.
Notes

    Ensure the spritesheet and the utility script are in the same directory or provide the correct file path.
    Adjust the width and height parameters based on your desired frame size.
