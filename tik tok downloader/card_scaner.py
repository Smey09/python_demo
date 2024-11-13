# card_scaner.py

from PIL import Image
import pytesseract
import re

def scan_card():
    # Define the image path
    image_path = 'khmer_Card.jpeg'
    
    try:
        # Open the image file
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return
    
    # Use pytesseract to extract text from the image
    raw_text = pytesseract.image_to_string(image)
    
    # Display the raw extracted text for verification
    print("Extracted Text:\n", raw_text)

    # Clean the text by removing unwanted characters
    cleaned_text = raw_text.replace('<', '')
    lines = cleaned_text.splitlines()  # Split text into lines

    # Initialize default values for extracted information
    id_user = None
    user_name = None
    card_type = None
    card_role = None

    # Regular expressions to match each field in the text
    id_user_pattern = re.compile(r'IDKHM\d{11}')         # Pattern: 'IDKHM' followed by 11 digits
    user_name_pattern = re.compile(r'\d{7}[A-Z]\d{7}KHM')  # Pattern: 7 digits, 1 letter, 7 digits, 'KHM'
    card_type_pattern = re.compile(r'\d[A-Z]{2}')         # Pattern: 1 digit followed by 2 letters
    card_role_pattern = re.compile(r'[A-Z]{7}')           # Pattern: exactly 7 letters

    # Search through each line for matches based on the patterns
    for line in lines:
        if not id_user and id_user_pattern.search(line):
            id_user = id_user_pattern.search(line).group()
        if not user_name and user_name_pattern.search(line):
            user_name = user_name_pattern.search(line).group()
        if not card_type and card_type_pattern.search(line):
            card_type = card_type_pattern.search(line).group()
        if not card_role and card_role_pattern.search(line):
            card_role = card_role_pattern.search(line).group()

    # Print the extracted information
    print("ID User:", id_user if id_user else "Not found")
    print("User Name:", user_name if user_name else "Not found")
    print("Card Type:", card_type if card_type else "Not found")
    print("Card Role:", card_role if card_role else "Not found")

    # Save the scanned image to a new file, only once
    scanned_image_path = 'scanned_khmer_card_extracted.png'
    image.save(scanned_image_path)
    print(f"Scanned image saved as: {scanned_image_path}")
