import time
from luma.led_matrix import create_8x8_matrix

def create_matrix():
    # Adjust parameters based on your LED matrix configuration
    return create_8x8_matrix()

def clear_matrix(matrix):
    matrix.clear()

def draw_ball(matrix, x, y):
    matrix.point((x, y), fill="white")

def bounce_ball(matrix, initial_x=3, initial_y=3, speed=0.1):
    x, y = initial_x, initial_y
    x_direction, y_direction = 1, 1

    while True:
        clear_matrix(matrix)
        draw_ball(matrix, x, y)
        matrix.show()

        time.sleep(speed)

        x += x_direction
        y += y_direction

        if x == 7 or x == 0:
            x_direction *= -1

        if y == 7 or y == 0:
            y_direction *= -1

if __name__ == "__main__":
    matrix = create_matrix()

    try:
        bounce_ball(matrix)
    except KeyboardInterrupt:
        clear_matrix(matrix)
        matrix.show()
