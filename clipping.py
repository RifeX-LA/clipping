def read_ints_line(file) -> list:
    return [int(i) for i in file.readline().split()]


def read_points(file, count: int) -> list:
    points = []
    for _ in range(count):
        args = read_ints_line(file)
        points.append(tuple(args))

    return points


def read_data(path: str) -> tuple:
    file = open(path)
    poly_type = file.readline().strip()
    count = int(file.readline())

    points = read_points(file, count)
    x1, y1, x2, y2 = read_ints_line(file)
    rect = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]

    return poly_type, rect, points


def clip_segment(rect: list, x1, y1, x2, y2):
    x_min, y_min = rect[0]
    x_max, y_max = rect[2]

    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8

    def compute_outcode(x, y):
        code = INSIDE
        if x < x_min:
            code |= LEFT
        elif x > x_max:
            code |= RIGHT
        if y < y_min:
            code |= BOTTOM
        elif y > y_max:
            code |= TOP
        return code

    outcode1 = compute_outcode(x1, y1)
    outcode2 = compute_outcode(x2, y2)
    accept = False

    while True:
        if not (outcode1 | outcode2):
            accept = True
            break
        elif outcode1 & outcode2:
            break
        else:
            outcode_out = outcode1 if outcode1 else outcode2

            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2)

    if accept:
        return x1, y1, x2, y2
    else:
        return None


#
# midpoint algorithm
#
def segments_clipping(rect: list, segments: list) -> list:
    clipped_lines = []
    for x1, y1, x2, y2 in segments:
        clipped_line = clip_segment(rect, x1, y1, x2, y2)
        if clipped_line:
            clipped_lines.append(clipped_line)

    return clipped_lines


#
# polygon clipping algorithm
#
def is_inside(p1, p2, q):
    R = (p2[0] - p1[0]) * (q[1] - p1[1]) - (p2[1] - p1[1]) * (q[0] - p1[0])
    if R <= 0:
        return True
    else:
        return False


def compute_intersection(p1, p2, p3, p4):
    # if first line is vertical
    if p2[0] - p1[0] == 0:
        x = p1[0]

        # slope and intercept of second line
        m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
        b2 = p3[1] - m2 * p3[0]

        # y-coordinate of intersection
        y = m2 * x + b2

    # if second line is vertical
    elif p4[0] - p3[0] == 0:
        x = p3[0]

        # slope and intercept of first line
        m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b1 = p1[1] - m1 * p1[0]

        # y-coordinate of intersection
        y = m1 * x + b1

    # if neither line is vertical
    else:
        m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
        b1 = p1[1] - m1 * p1[0]

        # slope and intercept of second line
        m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
        b2 = p3[1] - m2 * p3[0]

        # x-coordinate of intersection
        x = (b2 - b1) / (m1 - m2)

        # y-coordinate of intersection
        y = m1 * x + b1

    intersection = (x, y)

    return intersection


def polygon_clipping(clipping_polygon, subject_polygon):
    final_polygon = subject_polygon.copy()

    for i in range(len(clipping_polygon)):

        # stores the vertices of the next iteration of the clipping procedure
        next_polygon = final_polygon.copy()

        # stores the vertices of the final clipped polygon
        final_polygon = []

        # these two vertices define a line segment (edge) in the clipping
        # polygon. It is assumed that indices wrap around, such that if
        # i = 1, then i - 1 = K.
        c_edge_start = clipping_polygon[i - 1]
        c_edge_end = clipping_polygon[i]

        for j in range(len(next_polygon)):

            # these two vertices define a line segment (edge) in the subject
            # polygon
            s_edge_start = next_polygon[j - 1]
            s_edge_end = next_polygon[j]

            if is_inside(c_edge_start, c_edge_end, s_edge_end):
                if not is_inside(c_edge_start, c_edge_end, s_edge_start):
                    intersection = compute_intersection(s_edge_start, s_edge_end, c_edge_start, c_edge_end)
                    final_polygon.append(intersection)
                final_polygon.append(tuple(s_edge_end))
            elif is_inside(c_edge_start, c_edge_end, s_edge_start):
                intersection = compute_intersection(s_edge_start, s_edge_end, c_edge_start, c_edge_end)
                final_polygon.append(intersection)

    return final_polygon
