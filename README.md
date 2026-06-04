# Selective Image and Text Encryption

## Brief One Line Summary

A Python-based security application that selectively encrypts and decrypts image and text data to protect sensitive information.

---

## Overview

This project implements selective encryption techniques for both images and text files. Instead of encrypting all data, the system selectively encrypts important content, reducing computational overhead while maintaining security. The application demonstrates secure data protection using Python and cryptographic operations.

---

## Problem Statement

With the increasing exchange of digital data, protecting sensitive images and textual information has become essential. Traditional encryption methods can be computationally expensive for large datasets. This project aims to provide an efficient solution by selectively encrypting critical portions of image and text data while ensuring confidentiality and integrity.

---

## Dataset

The project uses sample input files:

- Image File: `image.jpg`
- Text File: `Text.txt`

Generated files:

- `encrypted_image.png`
- `encrypted_text.txt`
- `decrypted_image.png`
- `decrypted_text.txt`

---

## Tools and Technologies

- Python
- NumPy
- File Handling
- Cryptography Concepts
- Image Processing

---

## Methods

1. Read input image and text files.
2. Generate an encryption key.
3. Apply selective encryption on image data.
4. Encrypt textual information.
5. Store encrypted outputs securely.
6. Decrypt data using the generated key.
7. Verify the integrity of decrypted outputs.

---

## Key Insights

- Selective encryption reduces processing time compared to full encryption.
- Sensitive image and text data can be protected effectively.
- Encryption keys play a critical role in maintaining security.
- The decrypted outputs accurately reconstruct the original data.

---

## Model / Output

### Input Files

- image.jpg
- Text.txt

### Encrypted Outputs

- encrypted_image.png
- encrypted_text.txt

### Decrypted Outputs

- decrypted_image.png
- decrypted_text.txt

### Encryption Key

- encryption_key.npy

---

## How to Run This Project?

### Clone Repository

```bash
git clone https://github.com/yourusername/selective-image-and-text-encryption.git
cd selective-image-and-text-encryption
```

### Install Dependencies

```bash
pip install numpy pillow
```

### Run the Project

```bash
python main.py
```

### Output

The program generates:

```text
encrypted_image.png
encrypted_text.txt
decrypted_image.png
decrypted_text.txt
encryption_key.npy
```

---

## Results & Conclusion

The project successfully encrypts and decrypts image and text data using a selective encryption approach. The generated outputs demonstrate that sensitive information can be protected while maintaining efficiency and reducing computational complexity.

---

## Future Work

- Integrate advanced cryptographic algorithms such as AES.
- Develop a graphical user interface (GUI).
- Add support for multiple image formats.
- Enable secure cloud storage integration.
- Implement real-time encryption and decryption.

---

## Author & Contact

**Naima**

Bachelor of Engineering – Information Science and Engineering

GitHub: https://github.com/Naima457664


---
