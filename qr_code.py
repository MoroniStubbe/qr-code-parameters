import cv2
import numpy as np
from PIL import Image
import qrcode
from pyzbar.pyzbar import decode
    
def get_straight_qr_code(image):
    # Step 2: Use OpenCV's QR code detector to extract the raw pixel matrix
    qr_decoder = cv2.QRCodeDetector()
    
    # Use the `detectAndDecode()` method to extract the QR code and its data
    retval, points, straight_qrcode = qr_decoder.detectAndDecode(image)

    # If no QR code is found, raise an error
    if not retval:
        raise ValueError("No QR code detected in the image.")

    return straight_qrcode

def resize_qr_code_to_standard(image, scale_factor=2):
    straight_qrcode = get_straight_qr_code(image)

    # Step 3: Add a white border (value 255) around the matrix
    # `straight_qrcode` is already the raw QR code matrix
    bordered_matrix = np.pad(straight_qrcode, pad_width=1, mode='constant', constant_values=255)

    # Step 4: Convert the matrix to an image
    qr_image = Image.fromarray(bordered_matrix.astype(np.uint8))  # Convert to uint8 type for image processing
    
    # Calculate the new size by multiplying the current size by the scale factor
    new_width = qr_image.width * scale_factor
    new_height = qr_image.height * scale_factor
    new_size = (new_width, new_height)
    
    # Resize the image by the scale factor
    return qr_image.resize(new_size, Image.NEAREST)  # Use NEAREST to preserve the QR code structure

def get_raw_decoded_qr_code_data(image):
    # Decode the QR code from the image
    decoded_objects = decode(image)
    
    if decoded_objects:
        # The decoded object contains raw byte data in the 'data' field
        raw_data = decoded_objects[0].data
        print("Raw encoded QR code matrix extracted successfully.")
        return raw_data
    else:
        print("No QR code found in the image.")
        return None

def generate_qr_code(data, version, error_correction, mask, box_size=2, border=1):
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        mask_pattern=mask,
        box_size=box_size,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

def brute_force_qr_parameters(image_path):
    cv2_image = cv2.imread(image_path)
    PIL_image = Image.open(image_path)
    straight_qrcode = get_straight_qr_code(cv2_image)
    data = get_raw_decoded_qr_code_data(PIL_image)
    print(f"Decoded data from the original QR code: {data}")

    # Define the ranges of parameters to test
    versions = range(1, 41)  # QR code versions (1 to 40)
    error_corrections = [
        qrcode.constants.ERROR_CORRECT_L,
        qrcode.constants.ERROR_CORRECT_M,
        qrcode.constants.ERROR_CORRECT_Q,
        qrcode.constants.ERROR_CORRECT_H,
    ]
    masks = range(0, 8)

    # Iterate through all combinations of parameters
    for version in versions:
        for error_correction in error_corrections:
            for mask in masks:
                print(f"generating v={version} e={error_correction} m={mask}")

                # Generate QR code with the current parameters
                generated_image = generate_qr_code(data, version, error_correction, mask)
                generated_image.save("temp.png")
                generated_image = cv2.imread("temp.png")
                generated_straight_qrcode = get_straight_qr_code(generated_image)
                # Compare the raw matrices
                if (
                    generated_straight_qrcode is not None
                    and np.array_equal(straight_qrcode, generated_straight_qrcode)
                ):
                    print(f"Match found with parameters: "
                            f"Version={version}, "
                            f"Error Correction={error_correction}",
                            f"Mask={mask}")
                    return {
                        "version" : version,
                        "error_correction" : error_correction,
                        "mask" : mask
                    }

    print("No matching parameters found.")
    return None