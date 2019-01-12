import cv2
from functools import wraps
import json
import datetime
import numpy as np
import time
import statistics
import serial
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
from subprocess import call

_DEFAULT_POOL = ThreadPoolExecutor()
def threadpool(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        return (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)

    return wrap


BLACK = [0,0,0]
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout = 0.5)
time.sleep(1)
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def writer(input):
    arduino.write(str(input).encode())


def try1():
    global net
    count = 0
    counter = 0
    disp_count = 0
    frq = 5
    disp_frq = 3
    stream1 = cv2.VideoCapture(4)
    stream1.set(6, cv2.VideoWriter_fourcc('Y','U', 'Y', 'V'))
    #stream1.set(3,680)
    #stream1.set(4,360)
    stream2 = cv2.VideoCapture(2)
    stream2.set(6, cv2.VideoWriter_fourcc('Y','U', 'Y', 'V'))
    #stream2.set(3,680)
    #stream2.set(4,360)

    fourcc = cv2.VideoWriter_fourcc('H','2', '6', '4')
    #cv2.namedWindow("Disparity Map", cv2.WINDOW_NORMAL)

    bsize = 5

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

    confidence_val = 0

    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class

    # load the input image and construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    # (note: normalization is done via the authors of the MobileNet SSD
    # implementation)

    # pass the blob through the network and obtain the detections and
    # predictions

    while(stream1.isOpened()):
        ret1, frame1 = stream1.read()
        ret2, frame2 = stream2.read()
        if ret1==True:
            cv2.imshow('left',frame1)
            #cv2.imshow('right',frame2)

            # compute disparity
            if disp_count == disp_frq:
                disparity = stereo.compute(frame1, frame2).astype(np.float32) / 16.0
                disparity = (disparity-min_disp)/num_disp
                #cv2.imshow('Disparity Map', disparity)
                disp_count = 0
            if counter == frq:
                counter = 0
                image = intelligence(frame2.copy(), disparity.copy())
            #cv2.imshow("Output", image)

            counter += 1
            disp_count += 1

            if cv2.waitKey(1) & 0xFF == ord('c'):
                cv2.imwrite('L'+str(count)+'.png', frame1)
                cv2.imwrite('R'+str(count)+'.png', frame2)
                cv2.imsave('D'+str(count)+'.png', disparity)
                print("captured " + 'L'+str(count)+'.png')
                count += 1

            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    stream1.release()
    cv2.destroyAllWindows()

# construct the argument parse and parse the arguments
@threadpool
def intelligence(image, disparity):
    global net
    left = 0
    right = 0
    middle = 0
    (h, w) = image.shape[:2]
    print(w)
    print("width)")
    left_ignore = 200
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    counter = 0
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    confidence_val = 0
    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > confidence_val:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            if idx==15:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                #print bounding box coordinates
                print((startX, startY, endX, endY))

                # display the prediction
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                print("[INFO] {}".format(label))
                cv2.rectangle(image, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                depthList = []
                for x in range(startX, endX):
                    for y in range(startY, endY):
                        try:
                            depthList.append(disparity[y][x])
                        except:
                            print('---------------------------------------------poop')

                depth = statistics.median(depthList)
                #depth = np.percentile(depthList, 75)
                if (startX + endX) / 2 < (w-left_ignore) / 3:
                    if depth < 0:
                        left = max(left, 1)
                        print("al")
                    elif depth < 0.12:
                        left = max(left, 1)
                        print("bl")
                    elif depth < 0.22:
                        left =  max(left, 1)
                        print("cl")
                    elif depth < 0.32:
                        left =  max(left, 2)
                        print("dl")
                    else:
                        left =  max(left, 3)
                        print("e")
                elif (startX + endX) / 2 < (w-left_ignore) * 2 / 3:
                    if depth < 0:
                        middle = max(middle, 1)
                        print("am")
                    elif depth < 0.12:
                        middle = max(middle, 1)
                        print("bm")
                    elif depth < 0.32:
                        middle =  max(middle, 1)
                        print("cm")
                    elif depth < 0.42:
                        middle =  max(middle, 2)
                        print("dm")
                    else:
                        middle =  max(middle, 3)
                        print("em")
                else:
                    if depth < 0:
                        right = max(right, 1)
                        print("ar")
                    elif depth < 0.12:
                        right = max(right, 1)
                        print("br")
                    elif depth < 0.22:
                        right =  max(right, 1)
                        print("cr")
                    elif depth < 0.32:
                        right =  max(right, 2)
                        print("dr")
                    else:
                        right =  max(right, 3)
                        print("er")
                print("DEPTH" + str(depth))
    print("setting the values finally)")
    #writer(middle)
    #writer(left + 4)
    #writer(right + 9)
    num = (right << 4) + ((left) << 2) + ((middle))
    writer(num)
    #writer(3 + 4)
    #writer(3 + 9)
    print(str(left) + " " + str(middle) + "  " + str(right))
    return image

# show the output image
