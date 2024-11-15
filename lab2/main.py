import cv2
import numpy as np
from tkinter import Tk, Button, filedialog, Label, Frame
from PIL import Image, ImageTk

# Define the kernel for morphological operations
kernel = np.ones((3, 3), np.uint8)

# Define maximum display size for the image
MAX_IMAGE_SIZE = (450, 450)

# Initialize variables for original and current images
image = None
original_image = None


# Function for high-frequency sharpening applied separately to each color channel
def apply_sharpening(image):
    sharp_kernel = np.array([[0, -0.5, 0],
                             [-0.5, 3, -0.5],
                             [0, -0.5, 0]])
    # Split image into color channels
    b, g, r = cv2.split(image)
    # Apply Gaussian Blur and sharpening to each channel separately
    b_sharp = np.clip(cv2.filter2D(b, -1, sharp_kernel), 0, 255)
    g_sharp = np.clip(cv2.filter2D(g, -1, sharp_kernel), 0, 255)
    r_sharp = np.clip(cv2.filter2D(r, -1, sharp_kernel), 0, 255)
    # Merge channels back
    return cv2.merge((b_sharp, g_sharp, r_sharp)).astype(np.uint8)


# Function to convert OpenCV image to tkinter-compatible format with resizing
def cv2_to_tk(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for tkinter
    pil_image = Image.fromarray(image_rgb)
    pil_image.thumbnail(MAX_IMAGE_SIZE)  # Resize the image to fit within MAX_IMAGE_SIZE
    return ImageTk.PhotoImage(pil_image)


# Function to load the image
def load_image():
    global image, original_image, image_path, tk_image
    image_path = filedialog.askopenfilename()
    if image_path:
        image = cv2.imread(image_path)  # Load in color (BGR format)
        original_image = image.copy()   # Save a copy of the original image
        display_image(image)


# Function to display image in tkinter window
def display_image(image):
    global tk_image
    tk_image = cv2_to_tk(image)
    image_label.config(image=tk_image)
    image_label.image = tk_image


# Functions for morphological operations with sharpening
def apply_erosion():
    if image is not None:
        eroded_image = cv2.erode(image, kernel, iterations=1)
        sharpened_eroded = apply_sharpening(eroded_image)
        display_image(sharpened_eroded)


def apply_dilation():
    if image is not None:
        dilated_image = cv2.dilate(image, kernel, iterations=1)
        sharpened_dilated = apply_sharpening(dilated_image)
        display_image(sharpened_dilated)


def apply_opening():
    if image is not None:
        opening_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        sharpened_opening = apply_sharpening(opening_image)
        display_image(sharpened_opening)


def apply_closing():
    if image is not None:
        closing_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        sharpened_closing = apply_sharpening(closing_image)
        display_image(sharpened_closing)


# Function to reset the image to the original
def reset_image():
    global image
    if original_image is not None:
        image = original_image.copy()
        display_image(image)


# Initialize the Tkinter interface
root = Tk()
root.title("Morphological Operations with Sharpening")
root.geometry("600x700")  # Set window size

# Frame to hold the image and limit its size
image_frame = Frame(root, width=MAX_IMAGE_SIZE[0], height=MAX_IMAGE_SIZE[1])
image_frame.pack(pady=10)
image_label = Label(image_frame)
image_label.pack()

# Button to load image
load_button = Button(root, text="Load Image", command=load_image)
load_button.pack()

# Buttons for morphological operations
erosion_button = Button(root, text="Erode", command=apply_erosion)
erosion_button.pack()

dilation_button = Button(root, text="Dilation", command=apply_dilation)
dilation_button.pack()

opening_button = Button(root, text="Opening", command=apply_opening)
opening_button.pack()

closing_button = Button(root, text="Closing", command=apply_closing)
closing_button.pack()

# Button to reset image
reset_button = Button(root, text="Reset", command=reset_image)
reset_button.pack()

# Run the Tkinter loop
root.mainloop()
