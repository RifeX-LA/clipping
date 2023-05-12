from matplotlib import pyplot as plt


def draw_polygon(polygon: list, color: str = 'blue'):
    polygon.append(polygon[0])
    xs, ys = zip(*polygon)
    plt.plot(xs, ys, color=color)


def draw_lines(lines: list, color: str):
    for line in lines:
        x1, y1, x2, y2 = line
        plt.plot((x1, x2), (y1, y2), marker='o', color=color)


def draw_with_lines(polygon: list, lines: list, clipped_lines: list):
    draw_polygon(polygon)
    draw_lines(lines, 'black')
    draw_lines(clipped_lines, 'red')
    plt.show()


def draw_with_polygons(rect: list, polygon: list, clipped_polygon: list):
    draw_polygon(rect)
    draw_polygon(polygon, 'black')
    draw_polygon(clipped_polygon, 'red')
    plt.show()


def draw(poly_type: str, *args):
    draw_algorithm = draw_with_polygons if poly_type == 'polygon' else draw_with_lines
    draw_algorithm(*args)
