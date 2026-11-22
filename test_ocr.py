
import pytesseract
import fitz

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Check Tesseract
print("Tesseract version:")
print(pytesseract.get_tesseract_version())

# Open PDF
pdf = fitz.open("data/sample.pdf")

# Select page 13 (index 12)
page = pdf[12]

# Convert page into image
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

# Save temporary image
pix.save("data/test_page.png")

# Perform OCR
image = fitz.Pixmap("data/test_page.png")

from PIL import Image

img = Image.open("data/test_page.png")

text = pytesseract.image_to_string(img)

print("\n========== OCR RESULT ==========")
print(text)
