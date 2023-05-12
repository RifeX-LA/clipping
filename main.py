import clipping
import gui

if __name__ == '__main__':
    poly_type, rect, points = clipping.read_data('points.txt')
    clipping_algorithm = clipping.polygon_clipping if poly_type == 'polygon' else clipping.segments_clipping
    gui.draw(poly_type, rect, points, clipping_algorithm(rect, points))
