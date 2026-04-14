import time

from app.services.inference_service import start as start_inference
from app.services.document_service import start as start_document
from app.services.cli_service import submit_image

def main():
    start_inference()
    start_document()

    time.sleep(1)

    submit_image()

    time.sleep(3)

if __name__ == "__main__":
    main()