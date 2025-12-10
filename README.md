DualCipher – Simple Cryptography Application

A lightweight desktop application that performs Caesar Cipher and Vigenère Cipher encryption & decryption.
Built using Python and Tkinter, this tool helps users understand classical cryptography in a simple and interactive way.

🔐 Features

Caesar Cipher

Encrypt & decrypt text using a numeric shift key.

Vigenère Cipher (Polyalphabetic)

Encrypt & decrypt using an alphabetic key.

Clean UI

Input and output text areas.

Drop-down menus to select cipher and mode.

Utility Functions

Load plaintext from a file

Save encrypted output

Copy output text

Clear all fields

Swap input–output for easy reversing

🖥️ Tech Stack

Python 3.x

Tkinter (default GUI library)

Optional: pyperclip for enhanced clipboard support

📸 Preview
--------------------------------------------
| Cipher: Caesar   Mode: Encrypt   Key: 3  |
--------------------------------------------
| Input Text:                              |
|  HELLO WORLD                             |
--------------------------------------------
| Output Text:                             |
|  KHOOR ZRUOG                             |
--------------------------------------------

📁 Project Structure
DualCipher/
│── crypto_app.py     # Main application file
│── README.md         # Documentation
│── LICENSE           # (Optional) license file

🚀 How to Run
1. Install Python

Make sure Python 3.7+ is installed.

Check using:

python --version

2. (Optional) Install pyperclip
pip install pyperclip

3. Run the application
python crypto_app.py

🔧 Usage Instructions

Open the application.

Select your cipher:

Caesar

Vigenère

Select Encrypt or Decrypt mode.

Enter a key:

Integer for Caesar (example: 3)

Letters for Vigenère (example: KEY)

Type or paste your text.

Click Run to see results.

Use additional buttons:

Swap I/O

Load Input

Save Output

Copy Output

Clear All

📘 Example
Caesar Encryption

Plaintext:

HELLO


Key:

3


Output:

KHOOR

Vigenère Encryption

Plaintext:

ATTACKATDAWN


Key:

LEMON


Output:

LXFOPVEFRNHR

🛡️ Limitations

This app demonstrates classical cryptography, which is not secure against modern attacks.

For educational and academic purposes only.

📄 License

This project is free to use for academic and learning purposes.

👤 Author

Anusha T.E
BMS Institute of Technology & Management
Cybersecurity / Computer Science Project
