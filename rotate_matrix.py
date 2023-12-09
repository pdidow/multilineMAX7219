# rotate_matrix.py
# Takes a matrix and degrees and returns rotated matrix
import numpy as np

def rotate_matrix(matrix, angle_degrees):
    radians = np.radians(angle_degrees)
    rotated_matrix = np.rot90(matrix, k=int(angle_degrees / 90))
    return rotated_matrix
