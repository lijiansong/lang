import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
'''
:                +------------------+
:                |                  |
:              height               |
:                |                  |
:             (x, y)---- width -----+
'''
ax.add_patch(
    patches.Rectangle(
        (0.1, 0.1),  # (x,y)
        0.5,  # width
        0.5,  # height
        color='r'))
ax.add_patch(
    patches.Rectangle(
        (0.2, 0.9),
        0.1,
        0.1,
        color='g'))
plt.show()
