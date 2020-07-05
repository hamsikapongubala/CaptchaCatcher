import os
import os.path
import cv2
import glob
import imutils

training_data_folder = "training_data"
output_folder = "extracted_letters"

#Get list of captcha images to process
captcha_image_files = glob.glob(os.path.join(training_data_folder, "*"))
counts = {}

#Loop over the images
for (i, captcha_image_file) in enumerate(captcha_image_files):
    print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))

    #Filename will contain the captcha text
    #Take the filename as text
    filename = os.path.basename(captcha_image_file)
    captcha_text = os.path.splitext(filename)[0]

    #Store BGR values of the file
    image = cv2.imread(captcha_image_file)
    
    #Convert the images to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Add extra padding around image
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)

    #Threshold the image (convert it to pure black and white)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    #Find the contours of the images
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = contours[1] if imutils.is_cv3() else contours[0]

    letter_image_regions = []

    #From the four contours loop through and extract the letters
    for contour in contours:
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)

        # Compare the width and height of the contour to detect letters that
        # are conjoined into one chunk
        if w / h > 1.25:
            # This contour is too wide to be a single letter
            # Split it in half into two letter region
            half_width = int(w / 2)
            letter_image_regions.append((x, y, half_width, h))
            letter_image_regions.append((x + half_width, y, half_width, h))
        else:
            # This is a normal letter by itself
            letter_image_regions.append((x, y, w, h))

    if len(letter_image_regions) != 4: #deleting bad training data
        continue

    # Sort the detected letters left-to-right
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

    # Save out each letter as a single image
    for letter_bounding_box, letter_text in zip(letter_image_regions, captcha_text):
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with 3 pixel margin
        letter_image = gray[y - 3:y + h + 3, x - 3:x + w + 3]

        # Get the folder to save the image in
        save_path = os.path.join(output_folder, letter_text)

        # if the output directory does not exist, create it
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # write the letter image to a file
        count = counts.get(letter_text, 1)
        p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
        cv2.imwrite(p, letter_image)

        # increment the count for the current key
        counts[letter_text] = count + 1

