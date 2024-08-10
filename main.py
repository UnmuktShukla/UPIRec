import pytesseract
import cv2
import PIL.Image
import requests
import re
from dateutil import parser
from word2number import w2n
import json

myconfig = r"--psm 6 --oem 1"

#cropping image to avoid reading screen time
image = cv2.imread('upi1.jpeg')
if image is None:
    print("Error: Image not loaded. Check your file path.")
    exit()
pixels_to_crop = 100
cropped_image = image[pixels_to_crop:, :]
cv2.imwrite('cropped_image.jpg', cropped_image)

#lll
text = pytesseract.image_to_string(PIL.Image.open("cropped_image.jpg"), config=myconfig)
textlis = text.split('\n')

print(textlis)
for i in textlis:
    ref =''
    for j in i:
        if j.isdigit() :
            ref= ref + str(j)
    if len(ref)==12 and ref.isdigit():
        print("reference id:",ref)

def find_times(text):
    pattern = r'\b([01]?[0-9]|2[0-3]):([0-5][0-9])\b'
    matches = re.findall(pattern, text)

    times = [f"{hour}:{minute}" for hour, minute in matches]
    return times


times = find_times(text)
print(times)



def extract_dates(text):
    # Define a pattern to identify possible date strings
    date_patterns = [
        r'\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\b',           # e.g., 23 January 2020
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',               # e.g., 01/23/2020 or 01/23/20
        r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',               # e.g., 01-23-2020 or 01-23-20
        r'\b\d{4}/\d{1,2}/\d{1,2}\b',                 # e.g., 2020/01/23
        r'\b\d{4}-\d{1,2}-\d{1,2}\b',                 # e.g., 2020-01-23
        r'\b\d{1,2}\s+[A-Za-z]{3,}\s+\d{4}\b',        # e.g., 23 Feb 2020
        r'\b[A-Za-z]{3,}\s+\d{1,2},\s+\d{4}\b',       # e.g., March 23, 2020
        r'\b[A-Za-z]{3,}\s+\d{1,2}\s+\d{4}\b',        # e.g., March 23 2020
        r'\b\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\b',         # e.g., 23 Mar 2020
        r'\b\d{1,2}\s+[A-Za-z]{3},\s+\d{4}\b',        # e.g., 23 Mar, 2020
        r'\b\d{1,2}-[A-Za-z]{3}-\d{4}\b',             # e.g., 23-Mar-2020
        r'\b\d{1,2}/[A-Za-z]{3}/\d{4}\b',             # e.g., 23/Mar/2020
        r'\b\d{4}-[A-Za-z]{3}-\d{1,2}\b'              # e.g., 2020-Mar-23

    ]

    dates = []


    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:

                parsed_date = parser.parse(match, fuzzy=True)

                dates.append(parsed_date.strftime("%d/%m/%Y"))
            except ValueError:

                continue

    return dates


found_dates = extract_dates(text)
print("Extracted Dates:", found_dates)
#AMOUNT





def detect_and_convert_amount(text):
    # Regular expression patterns to match amounts written in digits or words
    digit_pattern = r'\d+(?:\.\d+)?'  # Matches digits with optional decimal part
    word_pattern = r'(?:\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\w+teen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)\b\s*)+'  # Matches words representing numbers

    # Search for amounts written in digits
    digit_matches = re.findall(digit_pattern, text)
    digit_amounts = [float(match) for match in digit_matches]

    # Search for amounts written in words and convert them to digits
    word_matches = re.findall(word_pattern, text, re.IGNORECASE)
    word_amounts = [w2n.word_to_num(match) for match in word_matches]

    # Combine both digit and word amounts
    all_amounts = digit_amounts + word_amounts

    return all_amounts


# Example text containing amounts written in digits and words

amounts = detect_and_convert_amount(text)
print("Detected amounts:", amounts)
