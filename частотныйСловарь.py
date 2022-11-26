import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.morphology import erosion
from scipy.ndimage import morphology

def countLakesAndBays(region):
    symbol = ~region.image
    lb = label(symbol)
    lakes = 0
    bays = 0
    for reg in regionprops(lb):
        is_lake = True
        for y, x in reg.coords: 
            if y == 0 or x == 0 or y == region.image.shape[0] - 1 or x == region.image.shape[1] - 1:
                is_lake = False
                break
        lakes += is_lake
        bays += not is_lake             
    return lakes, bays


def has_vline(image): 
    return 1 in erosion(np.mean(image, 0), [1, 1, 1])

def has_hline(image): 
    return 1 in np.mean(image, 1)

def recognize(image_region):
    lakes, bays = countLakesAndBays(image_region)
    if lakes == 2: 
        if has_vline(image_region.image):
            return 'B'
        else:
            return '8'
    elif lakes == 1:
        if bays == 4:
            return '0'
        elif bays == 3:
            return 'A'
        elif bays == 2:
            rr, cc = image_region.centroid_local
            if(rr / image_region.image.shape[0] < 0.40 and cc / image_region.image.shape[1] < 0.40):
                return 'P'
                # print(rr / image_region.image.shape[0], cc / image_region.image.shape[1])
            else:
                return 'D'
    elif lakes == 0:
        if np.mean(image_region.image) == 1.0:
            return '-'
        elif has_vline(image_region.image):
            return '1'
        elif bays == 2:
            return '/'
        elif has_hline(image_region.image):
            return '*'
        elif bays == 4:
            return 'X'
        else:
            return 'W'
            



image = plt.imread("D:\\symbols.png")
image = np.mean(image,2)
image[image > 0] = 1 #бинаризация (так как не можем использовать label на небинариз.)
labeled = label(image)
regions = regionprops(labeled) #собираем символы
result = {}

for reg in regions:
    symbol = recognize(reg)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1 / np.max(labeled) * 100
for k, v in result.items():
    print("'" + str(k) + "'" + " : " + str(v) + "%")

plt.show()
