import cv2
import imutils
import numpy as np
import argparse

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


def argparser():
    arg_parse = argparse.ArgumentParser()
    # arg_parse.add_argument("-i", "--image", default=None, help="path to Image File ")
    arg_parse.add_argument("-c", "--confidence", type=float, default=0.35,
                           help="minimum probability to filter weak detections")
    arg_parse.add_argument("-d", "--detect", default="person",
                           help="what to detect")
    args = vars(arg_parse.parse_args())
    return args


def detection(img, confi, detect):
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe("detector/MobileNetSSD_deploy.prototxt.txt",
                                   "detector/MobileNetSSD_deploy.caffemodel")
    image = cv2.imread(img)
    image = imutils.resize(image, width=min(400, image.shape[1]))
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    person: int = 0

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > confi:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            if CLASSES[idx] == detect:
                label = "{}{}: {:.2f}%".format(CLASSES[idx], person + 1,
                                               confidence * 100)
                print(label)
                cv2.rectangle(image, (startX, startY), (endX, endY),
                              (25, 216, 94), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (25, 216, 94), 2)
                person += 1

    print(f'Total {detect}s : {person}')
    if person > 0:
        cv2.putText(image, f'Total {detect}s : {person}', (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 0, 0), 2)
        cv2.imshow(img, image)
        cv2.waitKey(0)
        cv2.destroyWindow(img)
