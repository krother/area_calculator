from models import Circle, Donut, Move, Square, Triangle


def test_move_changes_position_size_and_wraps_color():
    sq = Square(size=2, color=(255, 0, 0),
                move=Move(xspeed=1, yspeed=2, scale_mod=3, color_mod=(1, 0, 0)))
    sq.move.apply_move(sq)
    assert (sq.x, sq.y, sq.size, sq.color) == (129, 130, 5, (0, 0, 0))


def test_donut_scales_both_radii():
    d = Donut(radius=10, inner_radius=5)
    d.modify_scale(2)
    assert (d.radius, d.inner_radius) == (12, 7)


def test_circle_draw_uses_given_frame():
    import numpy as np
    frame = np.zeros((800, 1200, 3), np.uint8)
    Circle(x=50, y=50, radius=5, color=(9, 9, 9)).draw(frame)
    assert tuple(frame[50, 50]) == (9, 9, 9)


def test_triangle_edge_scale():
    t = Triangle.blue_upsidedown_triangle(0, 0)
    t.modify_scale(8)
    assert t.edge_length == 50
