import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import numpy as np
import base64, hashlib
from cryptography.fernet import Fernet

class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image and Text Encryptor")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)

        self.image_frame = tk.Frame(root)
        self.image_frame.pack(side="top", fill="x")

        self.text_frame = tk.Frame(root)
        self.text_frame.pack(side="bottom", fill="x")

        self.select_button = tk.Button(self.image_frame, text="Select Image", command=self.select_image)
        self.select_button.pack(side="left")

        self.encrypt_button = tk.Button(self.image_frame, text="Encrypt Selected Part", command=self.encrypt_part)
        self.encrypt_button.pack(side="left")

        self.decrypt_button = tk.Button(self.image_frame, text="Decrypt Selected Part", command=self.decrypt_part)
        self.decrypt_button.pack(side="left")

        self.select_text_button = tk.Button(self.text_frame, text="Select Text File", command=self.select_text_file)
        self.select_text_button.pack(side="left")

        self.encrypt_text_button = tk.Button(self.text_frame, text="Encrypt Text", command=self.encrypt_text)
        self.encrypt_text_button.pack(side="left")

        self.decrypt_text_button = tk.Button(self.text_frame, text="Decrypt Text", command=self.decrypt_text)
        self.decrypt_text_button.pack(side="left")

        self.region = None
        self.rect = None
        self.image = None
        self.image_array = None
        self.image_path = None
        self.text_file_path = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Generate encryption key
        passcode = '249524.405925.606329'
        self.key = self.gen_fernet_key(passcode.encode('utf-8'))
        self.cipher = Fernet(self.key)

    def gen_fernet_key(self, passcode: bytes) -> bytes:
        assert isinstance(passcode, bytes)
        hlib = hashlib.md5()
        hlib.update(passcode)
        return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

    def select_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.image_array = np.array(self.image)
            self.display_image(self.image)

    def display_image(self, image):
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_button_press(self, event):
        self.region = [(event.x, event.y)]

    def on_mouse_drag(self, event):
        if self.region:
            if self.rect:
                self.canvas.delete(self.rect)
            x1, y1 = self.region[0]
            x2, y2 = event.x, event.y
            self.rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")

    def on_button_release(self, event):
        if self.region:
            self.region.append((event.x, event.y))
            x1, y1 = self.region[0]
            x2, y2 = self.region[1]
            self.region = [(min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))]
            print(f"Selected region: {self.region}")

    def generate_key(self, shape):
        np.random.seed(0)  # for reproducibility
        return np.random.randint(0, 256, size=shape, dtype=np.uint8)

    def encrypt_part(self):
        if self.image_array is not None and self.region is not None:
            x1, y1 = self.region[0]
            x2, y2 = self.region[1]
            region_array = self.image_array[y1:y2, x1:x2]
            key = self.generate_key(region_array.shape)
            encrypted_array = np.bitwise_xor(region_array, key)
            self.image_array[y1:y2, x1:x2] = encrypted_array
            encrypted_image = Image.fromarray(self.image_array)
            encrypted_image.save("encrypted_image.png")
            self.display_image(encrypted_image)
            np.save('encryption_key.npy', key)

    def decrypt_part(self):
        if self.image_array is not None and self.region is not None:
            key = np.load('encryption_key.npy')
            x1, y1 = self.region[0]
            x2, y2 = self.region[1]
            encrypted_region_array = self.image_array[y1:y2, x1:x2]
            decrypted_array = np.bitwise_xor(encrypted_region_array, key)
            self.image_array[y1:y2, x1:x2] = decrypted_array
            decrypted_image = Image.fromarray(self.image_array)
            decrypted_image.save("decrypted_image.png")
            self.display_image(decrypted_image)

    def select_text_file(self):
        self.text_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        print(f"Selected text file: {self.text_file_path}")

    def encrypt_text(self):
        if self.text_file_path:
            keywords = simpledialog.askstring("Input", "Enter keywords to encrypt (comma-separated):")
            if keywords:
                keywords = [k.strip() for k in keywords.split(',')]
                encrypted_text = self.encrypt_text_file(self.text_file_path, keywords)
                with open("encrypted_text.txt", 'w') as file:
                    file.write(encrypted_text)
                print("Encrypted text saved as 'encrypted_text.txt'")

    def decrypt_text(self):
        if self.text_file_path:
            with open(self.text_file_path, 'r', encoding='utf-8') as file:
              encrypted_text= file.read()
            decrypted_text = self.decrypt_text_file(encrypted_text)
            with open("decrypted_text.txt", 'w') as file:
                file.write(decrypted_text)
            print("Decrypted text saved as 'decrypted_text.txt'")

    def encrypt_text_file(self, file_path, keywords):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        for keyword in keywords:
            encrypted_keyword = self.cipher.encrypt(keyword.encode()).decode()
            text = text.replace(keyword, encrypted_keyword)
        return text

    def decrypt_text_file(self, text):
        words = text.split()
        for word in words:
            try:
                decrypted_word = self.cipher.decrypt(word.encode()).decode()
                text = text.replace(word, decrypted_word)
            except:
                pass
        return text

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
