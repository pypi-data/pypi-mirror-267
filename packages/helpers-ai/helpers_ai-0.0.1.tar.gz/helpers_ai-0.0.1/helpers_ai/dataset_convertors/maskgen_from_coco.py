from pycocotools.coco import COCO
import os
import tqdm
import numpy as np
import cv2
# import matplotlib.pyplot as plt

def generate(json_path,destination):

    coco = COCO(json_path)
    imgid = coco.getImgIds()
    cat = coco.loadCats(coco.getCatIds())
    categ = [ct["name"] for ct in cat]
    corrupted = []
    image = coco.loadImgs(2)[0]
    print(image)

    ann = coco.loadAnns(coco.getAnnIds(2))
    print(len(ann))
    blank = np.zeros((image["height"],image["width"],3),dtype=np.int32)
    print(blank.shape)
    blank = cv2.cvtColor(blank,cv2.COLOR_BGR2GRAY)
    color = [200,120,20,90]
    for idx,i in enumerate(ann):
        seg = i["segmentation"][0]
        seg_x = seg[::2]
        seg_y = seg[1::2]
        f_seg = [[int(a),int(b)] for a,b in zip(seg_x,seg_y)]
        cv2.fillPoly(blank,[np.array(f_seg)],(color[idx],255,255),1)
    print(blank.shape)
    img = cv2.cvtColor(blank,cv2.COLOR_HSV2BGR)
    cv2.imshow("img",img)
    cv2.waitKey(0)
    # plt.imshow(blank)
    # plt.show()
        

# generate("D:/Data_set/minicoco/test_annotations/coco_labels.json",None)