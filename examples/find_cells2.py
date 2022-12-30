import cv2

# Load the image and convert it to grayscale
image = cv2.imread("cells.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a blur or smoothing filter to the image
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use a thresholding method to identify the cells
ret, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

# Find the contours of the cells
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw a line around each cell
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the image with the lines drawn
cv2.imshow("Cells", image)
cv2.waitKey(0)
