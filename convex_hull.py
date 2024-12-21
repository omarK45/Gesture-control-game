
import math
import numpy as np

# Utility function to calculate the orientation of three points (p, q, r)
# It returns a positive value if p-q-r makes a counter-clockwise turn,
# negative if clockwise, and 0 if the points are collinear.
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    return val

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# (Graham Scan)
def convex_hull(points):
    points = [(p[0][0], p[0][1]) if isinstance(p[0], np.ndarray) else tuple(p[0]) for p in points]

    points = sorted(points)
    lower = []
    for p in points:
        while len(lower) >= 2 and orientation(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and orientation(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    return lower[:-1] + upper[:-1]