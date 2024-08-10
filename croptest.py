import cv2

# Load the image
image = cv2.imread('upi2.jpeg')  # Replace 'path_to_your_image.jpg' with your image file

# Check if image has loaded properly
if image is None:
    print("Error: Image not loaded. Check your file path.")
    exit()

# Define how many pixels to crop from the top
pixels_to_crop = 100  # Change this value based on your needs

# Crop the image
# image[start_row:end_row, start_col:end_col]
cropped_image = image[pixels_to_crop:800, :]  # This keeps all columns but starts from 'pixels_to_crop' row

# Display the original and cropped images
cv2.imshow('Original Image', image)
cv2.imshow('Cropped Image', cropped_image)
cv2.waitKey(0)  # Wait for a key press to close the images
cv2.destroyAllWindows()

# Optionally save the cropped image
cv2.imwrite('cropped_image.jpg', cropped_image)
