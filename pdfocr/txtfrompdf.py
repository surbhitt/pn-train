import os
import time

try:
    from pdf2image import convert_from_path
    from pytesseract import image_to_data, image_to_string
except Exception as ex:
    print("requires pdf2image and pytersseract")
    exit(1)

input_folder = "input"
output_folder = "output"
fmt = "png"

pdfs = []

for file_name in os.listdir(input_folder):
    if os.path.isfile(os.path.join(input_folder, file_name)) and file_name.endswith(".pdf"):
        pdfs.append(file_name)

for pdf in pdfs:
    start_conv = time.time()
    # image filtering &
    # improving conrast brightness etc params might lead to accuracy inc
    images = convert_from_path(os.path.join(input_folder, pdf), fmt=fmt, first_page=None, last_page=None)
    end_conv = time.time()
    print(f"converted {pdf}")
    print(f"conversion time: {end_conv-start_conv}")

    start_ext = time.time()
    for image in images:
        f = open(os.path.join(output_folder, f"{pdf}.txt"), "a")
        print(image_to_string(image), file=f)
        f.close()
    end_ext = time.time()
    print(f"extraction time: {end_ext-start_ext}")
