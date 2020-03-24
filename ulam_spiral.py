import numpy as np
import cv2


def draw_ulam_spiral(size):
    spiral, mask, image, center = init_ulam_spiral(size)
    x = center - 1
    y = center + 1
    current = 3

    while True:
        pts_x, pts_y = mask_filter(x, y, mask, size)
        if len(pts_x) == 0:
            break

        min_x, min_y = find_next(pts_x, pts_y, center)
        current = current + 1
        x = min_x
        y = min_y

        spiral[x][y] = current
        mask[x][y] = 1
        print(current)
        if is_prime(current):
            image[x][y] = 0

    cv2.imwrite("ulam_spiral.jpg", image)


def init_ulam_spiral(size):
    spiral = np.zeros((size, size), np.uint8)
    mask = np.zeros((size, size), np.uint8)
    image = np.ones((size, size), np.uint8) * 255
    center = size // 2

    spiral[center][center] = 1
    spiral[center][center + 1] = 2
    spiral[center - 1][center + 1] = 3

    mask[center][center] = 1
    mask[center][center + 1] = 1
    mask[center - 1][center + 1] = 1

    image[center][center] = 0
    image[center][center + 1] = 1
    image[center - 1][center + 1] = 1

    return spiral, mask, image, center


def mask_filter(x, y, mask, size):
    pts_x = []
    pts_y = []

    if (-1 < x < size) and (-1 < y + 1 < size) and mask[x][y + 1] == 0:
        pts_x.append(x)
        pts_y.append(y + 1)
    if (-1 < x - 1 < size) and (-1 < y < size) and mask[x - 1][y] == 0:
        pts_x.append(x - 1)
        pts_y.append(y)
    if (-1 < x < size) and (-1 < y - 1 < size) and mask[x][y - 1] == 0:
        pts_x.append(x)
        pts_y.append(y - 1)
    if (-1 < x + 1 < size) and (-1 < y < size) and mask[x + 1][y] == 0:
        pts_x.append(x + 1)
        pts_y.append(y)

    return pts_x, pts_y


def find_next(pts_x, pts_y, center):
    min_dist = (pts_x[0] - center) ** 2 + (pts_y[0] - center) ** 2
    min_x = pts_x[0]
    min_y = pts_y[0]

    for idx in range(1, len(pts_x)):
        dist = (pts_x[idx] - center) ** 2 + (pts_y[idx] - center) ** 2
        if dist < min_dist:
            min_dist = dist
            min_x = pts_x[idx]
            min_y = pts_y[idx]

    return min_x, min_y


def is_prime(value):
    if value < 2:
        return False
    for i in range(2, int(value ** 0.5 + 1)):
        if value % i == 0:
            return False
    return True


if __name__ == '__main__':
    draw_ulam_spiral(201)
