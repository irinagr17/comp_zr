import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage.measure import label, regionprops

def makeGroups(colors):
    delta = np.max(np.diff(colors)) / 2
    groups = [[colors[0]],]
    for i in range(1, len(colors)):
        previous = colors[i-1]
        current = colors[i]
        if current - previous > delta:
            groups.append([])
        groups[-1].append(current)
    return groups

image = plt.imread("C:\\Users\\cooli\\Downloads\\balls_and_rects.png")
hsv = color.rgb2hsv(image) #переводим в hsv
binary = hsv[:, :, 0].copy()
binary[binary > 0] = 1
labeled = label(binary)
regions = regionprops(labeled)

rectColors = []
ballColors = []
rectNumber = 0
ballNumber = 0
for reg in regions:
    cy, cx = reg.centroid #находим центр
    if np.mean(reg.image) == 1.0:
        rectColors.append(hsv[int(cy), int(cx), 0])
        rectNumber += 1
    else:
        ballColors.append(hsv[int(cy), int(cx), 0])
        ballNumber += 1

rectGroups = [[rectColors[0]],]
ballGroups = [[ballColors[0]],]
rectColors = sorted(rectColors)
ballColors = sorted(ballColors)

rectGroups = makeGroups(rectColors)
ballGroups = makeGroups(ballColors)

rectResult = dict()
ballResult = dict()
for grp in rectGroups:
    rectResult[np.mean(grp)] = len(grp)
for grp in ballGroups:
    ballResult[np.mean(grp)] = len(grp)

allFigeres = ballNumber + rectNumber

print("Всего фигур " + str(allFigeres))
print("Квадратов: " + str(rectNumber))
print(rectResult)
print("Кругов: " + str(ballNumber))
print(ballResult)