import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
from zipfile import ZipFile
import arabic_reshaper

# install: pip install python-bidi
from bidi.algorithm import get_display
# Constants for QR code and A4 paper dimensions
QR_CODE_SIZE_CM = 3     # Each QR code size in cm
PAGE_MARGIN_CM = 1    # Margin around the A4 paper in cm
A4_WIDTH_CM = 21        # A4 width in cm
A4_HEIGHT_CM = 29.7     # A4 height in cm
CM_TO_PIXELS = 600 / 2.54  # DPI for 600px resolution

# Calculate the size in pixels
qr_code_size_px = int(QR_CODE_SIZE_CM * CM_TO_PIXELS)
font_size_px = 50  
page_margin_px = int(PAGE_MARGIN_CM * CM_TO_PIXELS)
a4_width_px = int(A4_WIDTH_CM * CM_TO_PIXELS)
a4_height_px = int(A4_HEIGHT_CM * CM_TO_PIXELS)
qr_size_px = int(QR_CODE_SIZE_CM * CM_TO_PIXELS)
margin_px = int(PAGE_MARGIN_CM * CM_TO_PIXELS)

# Calculate how many QR codes fit on a page
num_qr_horizontal = int(a4_width_px / (qr_size_px + margin_px))
num_qr_vertical = int(a4_height_px / (qr_size_px + margin_px))
qr_per_page = num_qr_horizontal * num_qr_vertical
qr_code_size_px = int(QR_CODE_SIZE_CM * CM_TO_PIXELS)
font_size_px = 50  
page_margin_px = int(PAGE_MARGIN_CM * CM_TO_PIXELS)
a4_width_px = int(A4_WIDTH_CM * CM_TO_PIXELS)
a4_height_px = int(A4_HEIGHT_CM * CM_TO_PIXELS)


def generate_qr_pages(num_pages):
    pages_folder = "/mnt/data/qr_pages"
    os.makedirs(pages_folder, exist_ok=True)
    
    for page_number in range(num_pages):
        a4_page = Image.new('RGB', (a4_width_px + 1 * page_margin_px, a4_height_px + 1 * page_margin_px), 'white')
        draw = ImageDraw.Draw(a4_page)
        font = ImageFont.truetype("AbarHighFaNum-Bold.ttf", 50)  # Set the font size

        for i in range(qr_per_page):
            qr_index = page_number * qr_per_page + i
            if qr_index >= 999:
                break
            num = f"{qr_index + 1:03}"
            url = f"http://specificdomain.ir/?qr={num}"

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill='black', back_color='white')
            qr_img = qr_img.resize((qr_size_px, qr_size_px), Image.LANCZOS)
            
            # Calculate position
            x = (i % num_qr_horizontal) * (qr_size_px + margin_px) + page_margin_px
            y = (i // num_qr_horizontal) * (qr_size_px + margin_px) + page_margin_px
            
            # Paste QR code on the page
            a4_page.paste(qr_img, (x, y))
            
            # Add number below the QR code
            draw.text(
                (x + qr_size_px / 2, y + qr_size_px + 50), 
                num, 
                font=font, 
                fill="black", 
                anchor="mm"
            )
            text = "کتابکندو"
            reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
            bidi_text = get_display(reshaped_text)  
            draw.text(
                (x + qr_size_px / 2, y + qr_size_px + 100), 
                bidi_text, 
                font=font, 
                fill="black", 
                anchor="mm"
            )  

          

        # Save the A4 page
        a4_page.save(f"{pages_folder}/A4_QR_Page_{page_number+1}.png")

    return pages_folder

# Generate the necessary number of pages
num_pages = (999 // qr_per_page) + 1  # Calculate total number of pages needed
pages_folder = generate_qr_pages(num_pages)

# Create a ZIP file containing all the A4 pages
zip_filename = "A4_QR_Pages.zip"
with ZipFile(zip_filename, 'w') as zipf:
    for root, dirs, files in os.walk(pages_folder):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), pages_folder))

zip_filename
