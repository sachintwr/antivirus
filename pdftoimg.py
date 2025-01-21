import os
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf_to_images(pdf_path, output_dir, filename_prefix, image_format='jpg', dpi=600):
    """
    Convert PDF pages to images with custom naming
    
    Parameters:
    pdf_path (str): Path to the PDF file
    output_dir (str): Directory to save the images
    filename_prefix (str): Prefix for the output image filenames
    image_format (str): Output image format ('jpg' or 'png')
    dpi (int): Resolution of output images
    """
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Convert PDF to images
        pages = convert_from_path(pdf_path, dpi=dpi)
        
        # Save each page as an image
        for i, page in enumerate(pages):
            # Create filename with custom prefix and page number
            # output_file = f"{filename_prefix}_page_{i+1}.{image_format}"
            output_file = f"{i+1}.{image_format}"
            output_path = os.path.join(output_dir, output_file)
            
            # Save the image
            if image_format.lower() == 'jpg':
                page.convert('RGB').save(output_path, 'JPEG')
            else:
                page.save(output_path, 'PNG')
            
            print(f"Saved: {output_file}")
            
        print(f"\nSuccessfully converted {len(pages)} pages to {image_format.upper()} format")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    pdf_path = r"C:\Users\Kcloud-PC\Downloads\LH-PVT-Product-Book-Letter-v1.0.pdf"
    output_dir = r"C:\Users\Kcloud-PC\Downloads\pdftest"
    filename_prefix = "1"
    # image_format = "jpg"  # or "png"
    image_format = "png"
    
    convert_pdf_to_images(pdf_path, output_dir, filename_prefix, image_format)

    # $Env:Path += ";C:\Program Files\poppler\Library\bin" # Add poppler to PATH
    # python pdftoimg.py # Run the script