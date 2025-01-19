import qr_code

# Example usage
input_image = input("Enter the input path for the QR code image (e.g., 'input_qr_code.png'): ")

if(0):
    output_image = input("Enter the output path to save the regenerated QR code (e.g., 'output_qr_code.png'): ")
    qr_code.resize_qr_code_to_standard(input_image, output_image)
else:
    result = qr_code.brute_force_qr_parameters(input_image)
    if result:
        print("Original QR code parameters:", result)
