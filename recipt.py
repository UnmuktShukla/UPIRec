import cv2
import pytesseract
import numpy

custom_config = r'--oem 3 --psm 6 -l eng+hin'
def is_dark(image_path, threshold=0.5):
    # Load the image
    img = cv2.imread(image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Compute histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    # Normalize histogram
    hist /= hist.sum()

    # Compute cumulative distribution function (CDF)
    cdf = hist.cumsum()

    # Determine if the image is dark-themed based on the CDF
    dark_percentage = cdf[int(256 * threshold)]

    return dark_percentage > 0.5  # Adjust this threshold as needed

def invert_image(image):
    if len(image.shape) == 2:  # Grayscale image
        inverted_image = 255 - image
    elif len(image.shape) == 3:  # Color image
        inverted_image = cv2.bitwise_not(image)
    else:
        raise ValueError("Unsupported image format")
    return inverted_image

img= cv2.imread('upi3.jpeg')
base_img= img.copy()
dark = is_dark('upi3.jpeg')
if dark:
    img = invert_image(img)
else:
    pass

gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (115, 15) , 0.0)
cv2.imwrite("upi_blur.png" ,blur )
thresh = cv2.threshold(blur ,0 ,255 , cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel  = cv2.getStructuringElement(cv2.MORPH_RECT , (5,26))
dilate = cv2.dilate(thresh , kernel, iterations=1)

cv2.imwrite("upi_dilate.png" ,dilate )
cv2.imwrite("upi_threshold.png" ,thresh )

cnts = cv2.findContours(dilate , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cents[1]

cnts = sorted(cnts,key = lambda x: cv2.boundingRect(x)[0])

i=0

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    roi = img[y:y + h, x:x + w]
    impath= "ROI/upi_roi"+str(i)+".png"
    #if h>35 and w>50:

    cv2.rectangle(img , (x,y) , (x+w, y+h),(36,255,12) , 2)
    cv2.imwrite(impath,roi )
    ocr_res = pytesseract.image_to_string(roi , config=custom_config)
    print(ocr_res)
    i=i+1
cv2.imwrite("upi_bounding.png" ,img )