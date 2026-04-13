import qrcode
from PIL import Image
import sys
import os

def generate_qr(url, filename="certificate_qr.png"):
    """
    Generates a high-quality QR code pointing to the specified URL.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate Image
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Save the file
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    img.save(out_path)
    print(f"QR code successfully generated and saved to: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_qr.py <PUBLIC_URL>")
        print("Example: python generate_qr.py https://mahacert.netlify.app")
        sys.exit(1)
        
    target_url = sys.argv[1]
    generate_qr(target_url)
