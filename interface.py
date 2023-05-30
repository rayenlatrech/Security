from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import base64
import LSB_Steganography as l
import MSB_Steganography as m

# Function to handle LSB encryption
def encrypt_lsb(image_path, message):
    encoded_image_path = image_path + ".enc.png"
    l.encode_lsb(image_path, message)
    img = Image.open(encoded_image_path)
    img.show()

# Function to handle LSB decryption
def decrypt_lsb(image_path, output_path):
    message = l.decode_lsb(image_path, output_path)
    messagebox.showinfo("Decrypted Message", message)

# Function to handle MSB encryption
def encrypt_msb(image_path, message):
    encoded_image_path = image_path + ".enc.png"
    m.encode_msb(image_path, message)
    img = Image.open(encoded_image_path)
    img.show()

# Function to handle MSB decryption
def decrypt_msb(image_path, output_path):
    message = m.decode_msb(image_path, output_path)
    messagebox.showinfo("Decrypted Message", message)

# Function to handle file selection for encryption
def select_file_encrypt():
    image_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("PNG files", "*.png")])
    if not image_path:
        return

    file_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("TXT files", "*.txt")])
    if not file_path:
        return

    with open(file_path, "rb") as f:
        file_data = f.read()

    message = base64.b64encode(file_data).decode("utf-8")

    if lsb_selected.get():
        encrypt_lsb(image_path, message)
    elif msb_selected.get():
        encrypt_msb(image_path, message)

# Function to handle file selection for decryption
def select_file_decrypt():
    image_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("PNG files", "*.png")])
    if not image_path:
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if not output_path:
        return

    if lsb_selected.get():
        decrypt_lsb(image_path, output_path)
    elif msb_selected.get():
        decrypt_msb(image_path, output_path)

# Initialize the GUI window
root = Tk()
root.title("VisualVault")

# Initialize the encryption/decryption frame
encrypt_decrypt_frame = LabelFrame(root, text="Encryption/Decryption", padx=10, pady=10)
encrypt_decrypt_frame.pack(padx=20, pady=20)

# Initialize the method selection frame
method_frame = LabelFrame(root, text="Steganography Method", padx=10, pady=10)
method_frame.pack(padx=20, pady=(0, 20))

# Create the buttons and check buttons
encrypt_button = Button(encrypt_decrypt_frame, text="Encrypt", command=select_file_encrypt)
encrypt_button.pack(side=LEFT, padx=(0, 10))
decrypt_button = Button(encrypt_decrypt_frame, text="Decrypt", command=select_file_decrypt)
decrypt_button.pack(side=LEFT)

lsb_selected = BooleanVar()
msb_selected = BooleanVar()
lsb_checkbutton = Checkbutton(method_frame, text="LSB", variable=lsb_selected)
lsb_checkbutton.pack(side=LEFT, padx=(0, 10))
msb_checkbutton = Checkbutton(method_frame, text="MSB", variable=msb_selected)
msb_checkbutton.pack(side=LEFT)

# Start the GUI loop
root.mainloop()
