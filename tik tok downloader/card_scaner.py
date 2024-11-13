from PIL import Image
import pytesseract
import re

# Load the image
image_path = 'khmer_Card.jpeg'
image = Image.open(image_path)

# Use pytesseract to extract text
raw_text = pytesseract.image_to_string(image)

# Display the raw text for verification
print("Extracted Text:\n", raw_text)

# Clean up the extracted text by removing unwanted '<' characters
cleaned_text = raw_text.replace('<', '')

# Split the cleaned text into lines for easier processing
lines = cleaned_text.splitlines()

# Initialize default values
id_user = None
user_name = None
card_type = None
card_role = None

# Regular expression patterns for each field
id_user_pattern = re.compile(r'IDKHM\d{11}')         # Matches 'IDKHM' followed by 11 digits
user_name_pattern = re.compile(r'\d{7}[A-Z]\d{7}KHM')  # Matches 7 digits, 1 letter, 7 digits, and 'KHM'
card_type_pattern = re.compile(r'\d[A-Z]{2}')         # Matches 1 digit followed by 2 letters
card_role_pattern = re.compile(r'[A-Z]{7}')           # Matches exactly 7 letters (e.g., BBBCCCC)

# Search through each line for matches to the patterns
for line in lines:
    if not id_user and id_user_pattern.search(line):
        id_user = id_user_pattern.search(line).group()
    if not user_name and user_name_pattern.search(line):
        user_name = user_name_pattern.search(line).group()
    if not card_type and card_type_pattern.search(line):
        card_type = card_type_pattern.search(line).group()
    if not card_role and card_role_pattern.search(line):
        card_role = card_role_pattern.search(line).group()

# Print the extracted and cleaned information
print("id_user:", id_user)
print("User Name:", user_name)
print("Card Type:", card_type)
print("Card Role:", card_role)

# Save the scanned image to a new file, only once
scanned_image_path = 'scanned_khmer_card_extracted.png'
image.save(scanned_image_path)

# Confirmation message
print(f"Scanned image saved as: {scanned_image_path}")
