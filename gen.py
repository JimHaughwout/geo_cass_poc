from random import uniform
import numpy as np

bounding_boxes = (
    ((1.1, 35.0), (-4.6, 39.0)),
    ((1.4, 31.0), (0.0, 36.0))
    )
'''
bounding_boxes = dict([
    (1, ((1,1),(1,2))), 
    (2,'b')
    ])
'''
print type(bounding_boxes)
print len(bounding_boxes)
print bounding_boxes[0][0][0]