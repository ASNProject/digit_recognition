import os
import glob
import cv2
import easyocr
import Utils
from Utils_Recognition import check1Line, correctNumber, correctCapital, checkOddEven, showText

imagePath = "1.jpeg"
reader = easyocr.Reader(['en'])
digitPoints = []

heightDigitPlate = 250

def main():
    for filename in glob.glob(imagePath+"*.jpg"):
        img = cv2.imread(filename)
        scale = round(heightDigitPlate / img.shape[0], 1)
        img = Utils.resize(img, scale)

        detail = reader.readtext(img)
        numberPlate = check1Line(img, detail)

        numberPlate, oddEven = digitNumber(numberPlate)

        img = showText(img, numberPlate, oddEven)

        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def digitNumber(numberPlate):
    numberPlate = correctCapital(numberPlate)

    oddEven = checkOddEven(numberPlate)

    return numberPlate, oddEven

def printDetail(numberPlate, datePlate, code, city, oddEven, month, year):
    print("---"*20)
    print("numberPlateFix:", numberPlate)
    print("datePlateFix:", datePlate)
    print("- city code:", code)
    print("- city:", city)
    print("- type:", oddEven)
    print("- month:", month)
    print("- year:", year)
    print("---"*20)

if __name__ == '__main__':
    # Calling main() function
    main()

