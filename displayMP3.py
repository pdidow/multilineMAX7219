import os
import curses
import multilineMAX7219 as LEDMatrix

def display_files(stdscr, current_index, files):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    for i, file_name in enumerate(files):
        x = width // 2 - len(file_name) // 2
        y = height // 2 - len(files) // 2 + i
        stdscr.addstr(y, x, file_name, curses.A_BOLD if i == current_index else curses.A_NORMAL)

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.refresh()

    # Initialize the LED matrix
    LEDMatrix.init()

    # Specify the directory containing your files
    directory_path = "MP3"

    # Get a list of files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    current_index = 0

    while True:
        display_files(stdscr, current_index, files)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_index = (current_index - 1) % len(files)
        elif key == curses.KEY_DOWN:
            current_index = (current_index + 1) % len(files)
        elif key == 10:  # Enter key
            selected_file = files[current_index]
            # Display the selected file on the LED matrix
            LEDMatrix.clear()
            #LEDMatrix.static_message(selected_file)
            LEDMatrix.scroll_message_horiz([selected_file], 1, 8)

            LEDMatrix.gfx_render()

if __name__ == "__main__":
    curses.wrapper(main)
