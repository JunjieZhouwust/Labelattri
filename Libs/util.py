
def compute_iou(rec1, rec2, trans=0):
    """
    computing IoU
    :param rec1: (x0, y0, x1, y1), which reflects
            (left, top, right, bottom)
    :param rec2: (x0, y0, x1, y1)
    :return: scala value of IoU
    """
    # computing area of each rectangles

    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])


    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])

    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return (intersect / S_rec1) * 1.0