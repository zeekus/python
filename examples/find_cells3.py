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

# Create a list to store the mouse click coordinates
vertices = []

# Set up a mouse event handler to capture clicks
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        vertices.append((x, y))

# Display the image and capture mouse clicks
cv2.imshow("Cells", image)
cv2.setMouseCallback("Cells", mouse_callback)
cv2.waitKey(0)

# Draw a vertex at each mouse click location
for v in vertices:
    cv2.circle(image, v, 3, (255, 0, 0), -1)

# Draw lines between the vertices to create a closed shape
cv2.polylines(image, [np.int32(vertices)], True, (0, 255, 0), 2)

# Display the image with the vertices drawn
cv2.imshow("Cells", image)
cv2.waitKey(0)
