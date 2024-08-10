import cv2
import pytesseract

# Read the image
image = cv2.imread("cropped_image.jpg")

# Apply preprocessing (e.g., convert to grayscale, thresholding)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Perform OCR with whitelist configuration
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,₹'
text = pytesseract.image_to_string(binary, config=custom_config)

# Print the recognized text
print(text)