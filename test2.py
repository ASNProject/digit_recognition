import cv2
import pytesseract
from pytesseract import Output
from utils import get_grayscale, thresholding, opening, canny

img_source = cv2.imread('assets/5.jpeg')

gray = get_grayscale(img_source)
thresh = thresholding(img_source)
opening_img = opening(img_source)
canny_img = canny(img_source)

for img in [img_source, gray, thresh, opening_img, canny_img]:
    d = pytesseract.image_to_data(img, output_type=Output.DICT, config='--psm 6 --oem 3')
    n_boxes = len(d['text'])

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result_digits = ""

        for i in range(n_boxes):
            if int(d['conf'][i]) > 60 and d['text'][i].isdigit():
                (text, x, y, w, h) = (d['text'][i], d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # show only digits
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                img = cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60 and d['text'][i].isdigit():
                result_digits += d['text'][i]

        # Print the concatenated digits without a newline
        print(result_digits)

        cv2.imshow('img', img)
        cv2.waitKey(0)
