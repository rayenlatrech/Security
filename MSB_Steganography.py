from PIL import Image
import base64
from tkinter import messagebox


def encode_msb(image_path, data):
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()

    if img.mode != "RGB":
        raise ValueError("Image mode must be RGB")

    data_len = len(data.encode('ascii'))
    max_size = img.size[0] * img.size[1] * 3 // 8

    if data_len > max_size:
        raise ValueError(f"Data too large for image (max {max_size} bytes)")

    bin_data = ''.join(format(ord(ch), '08b') for ch in data)

    index = 0
    for row in range(img.size[0]):
       for col in range(img.size[1]):
          r, g, b = pixels[row, col]

          if index < len(bin_data):
             r = (r & 127) | (int(bin_data[index]) << 7)
             g = (g & 127) | (int(bin_data[index + 1]) << 7) if index + 1 < len(bin_data) else g
             b = (b & 127) | (int(bin_data[index + 2]) << 7) if index + 2 < len(bin_data) else b
             pixels[row, col] = (r, g, b)
             index += 3

          else:
                img.save(f"{image_path}.enc.png")
                return

    img.save(f"{image_path}.enc.png")


def decode_msb(image_path, output_path):
    img = Image.open(image_path)
    pixels = img.load()

    if img.mode != "RGB":
        raise ValueError("Image mode must be RGB")

    bin_data = ""

    for row in range(img.size[0]):
       for col in range(img.size[1]):
          r, g, b = pixels[row, col]
          bin_data += str((r >> 7) & 1)
          bin_data += str((g >> 7) & 1)
          bin_data += str((b >> 7) & 1)


    data = ""

    for i in range(0, len(bin_data), 8):
        data += chr(int(bin_data[i:i + 8], 2))

    with open(output_path, 'w', encoding='latin-1') as f:
        decoded_data = base64.b64decode(data.encode('latin-1')).decode('latin-1')
        f.write(decoded_data)

    return output_path
