#!/usr/bin/env python3
"""
Simple Cryptography App
- Ciphers: Caesar, Vigenere
- Encrypt / Decrypt
- Preserve case & non-letters
- Load / Save text files, Copy result
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import string
import sys

try:
    import pyperclip
except ImportError:
    pyperclip = None

# ---------- cipher utilities ----------

def caesar_transform(text, key, mode='enc'):
    key = key % 26
    if mode == 'dec':
        key = -key
    out = []
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            o = chr((ord(ch) - ord(base) + key) % 26 + ord(base))
            out.append(o)
        else:
            out.append(ch)
    return ''.join(out)

def vigenere_transform(text, keystr, mode='enc'):
    if not keystr:
        return text
    key = [ord(c.lower()) - ord('a') for c in keystr if c.isalpha()]
    if not key:
        return text
    out = []
    j = 0
    for ch in text:
        if ch.isalpha():
            k = key[j % len(key)]
            shift = k if mode == 'enc' else -k
            base = 'A' if ch.isupper() else 'a'
            o = chr((ord(ch) - ord(base) + shift) % 26 + ord(base))
            out.append(o)
            j += 1
        else:
            out.append(ch)
    return ''.join(out)

# ---------- GUI ----------

class CryptoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Cryptography App")
        self.geometry("760x520")
        self._build_ui()

    def _build_ui(self):
        pad = 6

        # Top frame: options
        frm = ttk.Frame(self)
        frm.pack(fill='x', padx=pad, pady=(pad, 0))

        ttk.Label(frm, text="Cipher:").grid(row=0, column=0, sticky='w')
        self.cipher_var = tk.StringVar(value='Caesar')
        cipher_menu = ttk.OptionMenu(frm, self.cipher_var, 'Caesar', 'Caesar', 'Vigenere')
        cipher_menu.grid(row=0, column=1, sticky='w', padx=(4,12))

        ttk.Label(frm, text="Mode:").grid(row=0, column=2, sticky='w')
        self.mode_var = tk.StringVar(value='Encrypt')
        mode_menu = ttk.OptionMenu(frm, self.mode_var, 'Encrypt', 'Encrypt', 'Decrypt')
        mode_menu.grid(row=0, column=3, sticky='w', padx=(4,12))

        ttk.Label(frm, text="Key:").grid(row=0, column=4, sticky='w')
        self.key_entry = ttk.Entry(frm, width=20)
        self.key_entry.grid(row=0, column=5, sticky='w', padx=(4,12))
        ttk.Label(frm, text="(int for Caesar, letters for Vigenere)").grid(row=0, column=6, sticky='w')

        # Main text areas
        txt_frame = ttk.Frame(self)
        txt_frame.pack(fill='both', expand=True, padx=pad, pady=pad)

        # Plaintext / Input
        left = ttk.Frame(txt_frame)
        left.pack(side='left', fill='both', expand=True, padx=(0,6))
        ttk.Label(left, text="Input / Plaintext:").pack(anchor='w')
        self.input_text = tk.Text(left, wrap='word', height=18)
        self.input_text.pack(fill='both', expand=True)

        # Ciphertext / Output
        right = ttk.Frame(txt_frame)
        right.pack(side='left', fill='both', expand=True)
        ttk.Label(right, text="Output / Ciphertext:").pack(anchor='w')
        self.output_text = tk.Text(right, wrap='word', height=18, state='normal')
        self.output_text.pack(fill='both', expand=True)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x', padx=pad, pady=(0,pad))

        ttk.Button(btn_frame, text="Run", command=self.run_transform).pack(side='left', padx=4)
        ttk.Button(btn_frame, text="Swap I/O", command=self.swap_io).pack(side='left', padx=4)
        ttk.Button(btn_frame, text="Load Input...", command=self.load_input).pack(side='left', padx=4)
        ttk.Button(btn_frame, text="Save Output...", command=self.save_output).pack(side='left', padx=4)
        ttk.Button(btn_frame, text="Copy Output", command=self.copy_output).pack(side='left', padx=4)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side='right', padx=4)

        # Status
        self.status = ttk.Label(self, text="Ready")
        self.status.pack(fill='x', padx=pad, pady=(0,pad))

    # ---------- actions ----------
    def run_transform(self):
        inp = self.input_text.get('1.0', 'end-1c')
        cipher = self.cipher_var.get()
        mode = 'enc' if self.mode_var.get().lower().startswith('e') else 'dec'
        key_raw = self.key_entry.get().strip()

        if cipher == 'Caesar':
            try:
                k = int(key_raw)
            except:
                messagebox.showerror("Bad Key", "For Caesar, key must be an integer (shift).")
                return
            out = caesar_transform(inp, k, mode)
        else:  # Vigenere
            if not key_raw.isalpha():
                messagebox.showerror("Bad Key", "For Vigenere, key must contain only letters (A-Z).")
                return
            out = vigenere_transform(inp, key_raw, mode)

        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.insert('1.0', out)
        self.output_text.config(state='normal')
        self.status.config(text=f"Done: {cipher} ({'Encrypt' if mode=='enc' else 'Decrypt'})")

    def swap_io(self):
        a = self.input_text.get('1.0', 'end-1c')
        b = self.output_text.get('1.0', 'end-1c')
        self.input_text.delete('1.0', 'end')
        self.input_text.insert('1.0', b)
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.insert('1.0', a)
        self.status.config(text="Swapped I/O")

    def load_input(self):
        path = filedialog.askopenfilename(title="Open text file", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't read file: {e}")
            return
        self.input_text.delete('1.0', 'end')
        self.input_text.insert('1.0', data)
        self.status.config(text=f"Loaded: {path}")

    def save_output(self):
        path = filedialog.asksaveasfilename(title="Save output", defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not path:
            return
        data = self.output_text.get('1.0', 'end-1c')
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(data)
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't save file: {e}")
            return
        self.status.config(text=f"Saved: {path}")

    def copy_output(self):
        data = self.output_text.get('1.0', 'end-1c')
        if not data:
            return
        try:
            # try pyperclip if available; else use tkinter clipboard
            if pyperclip:
                pyperclip.copy(data)
            else:
                self.clipboard_clear()
                self.clipboard_append(data)
        except Exception:
            self.clipboard_clear()
            self.clipboard_append(data)
        self.status.config(text="Output copied to clipboard")

    def clear_all(self):
        if not messagebox.askyesno("Clear", "Clear input and output?"):
            return
        self.input_text.delete('1.0', 'end')
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        self.status.config(text="Cleared")

# ---------- run ----------

def main():
    # optional: check tkinter availability
    try:
        print("Starting Cryptography App GUI...")
        app = CryptoApp()
        print("GUI window opened. Close it to exit.")
        app.mainloop()
    except tk.TclError as e:
        print("GUI not available:", e, file=sys.stderr)
        print("You can still use the core functions in a terminal (see README).", file=sys.stderr)

if __name__ == "__main__":
    main()
