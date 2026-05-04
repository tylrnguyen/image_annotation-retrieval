import sys
import time

from app.services.inference_service import start as start_inference
from app.services.document_service import start as start_document
from app.services.upload_service import submit_image

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <image_path>")
        return

    image_path = sys.argv[1]

    start_inference()
    start_document()

    time.sleep(1)

    submit_image(image_path)

    time.sleep(3)

if __name__ == "__main__":
    main()