import numpy as np
import cv2
from matplotlib import pyplot as plt
from sklearn.preprocessing import normalize

def test(disp, bsize):
    imgL = cv2.imread('left.jpg',0)
    imgR = cv2.imread('right.jpg',0)

    stereo = cv2.StereoBM_create(numDisparities=disp, blockSize=bsize)
    disparity = stereo.compute(imgL,imgR)
    plt.imshow(disparity,'gray')
    plt.show()

def test2(disp, bsize):
    print('loading images...')
    imgL = cv2.imread('L2.jpg')  # downscale images for faster processing if you like
    imgR = cv2.imread('R2.jpg')
    # SGBM Parameters -----------------
    window_size = 15                     # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely

    left_matcher = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=disp,             # max_disp has to be dividable by 16 f. E. HH 192, 256
        blockSize=bsize,
        P1=8 * 3 * window_size ** 2,    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
        P2=32 * 3 * window_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=0,
        speckleRange=2,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )
    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)
    # FILTER Parameters
    lmbda = 80000
    sigma = 1.2
    visual_multiplier = 1.0

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)

    print('computing disparity...')
    displ = left_matcher.compute(imgL, imgR)  # .astype(np.float32)/16
    dispr = right_matcher.compute(imgR, imgL)  # .astype(np.float32)/16
    displ = np.int16(displ)
    dispr = np.int16(dispr)
    filteredImg = wls_filter.filter(displ, imgL, None, dispr)  # important to put "imgL" here!!!
    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    filteredImg = np.uint8(filteredImg)
    cv2.imshow('Disparity Map', filteredImg)
    cv2.waitKey()
    cv2.destroyAllWindows()

def test3():
    # disparity settings
    bsize = 5
    lname = "LEFTFILENAME"
    rname = "RIGHTFILENAME"
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
    image_left = cv2.imread(lname)
    image_right = cv2.imread(rname)

    # compute disparity
    disparity = stereo.compute(image_left, image_right).astype(np.float32) / 16.0
    disparity = (disparity-min_disp)/num_disp
