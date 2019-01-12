import numpy as np
import cv2
from matplotlib import pyplot as plt
from sklearn.preprocessing import normalize

def test3(bsize, lname, rname):
    # disparity settings
    window_size = 5
    min_disp = 32
    num_disp = 112-min_disp
    stereo = cv2.StereoSGBM_create(
        minDisparity = min_disp,
        numDisparities = num_disp,
        blockSize=bsize,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32,
        disp12MaxDiff = 1,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2
    )

    # morphology settings
    kernel = np.ones((12,12),np.uint8)
    counter = 450
    while counter < 650:
        # increment counter
        counter += 1
        # only process every third image (so as to speed up video)
        if counter % 3 != 0: continue
        # load stereo image
        filename = str(counter).zfill(4)
        image_left = cv2.imread(lname)
        image_right = cv2.imread(rname)
        # compute disparity
        disparity = stereo.compute(image_left, image_right).astype(np.float32) / 16.0
        disparity = (disparity-min_disp)/num_disp
        cv2.imshow('Disparity Map', disparity)
        cv2.waitKey()
        cv2.destroyAllWindows()
