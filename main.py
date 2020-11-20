#===========================
# Imports
#===========================

import tkinter as tk
from tkinter import ttk, colorchooser, Menu, Spinbox, scrolledtext as st, messagebox as mb, filedialog as fd

import pyperclip
import re

#===========================
# Main App
#===========================

class App(tk.Tk):
    """Main Application."""

    #===========================================
    def __init__(self):
        super().__init__()
        self.init_config()

        self.phone_regex = re.compile(r'''(
            (\d{3}|\(\d{3}\))?              # area code
            (\s|-|\.)?                      # separator
            (\d{3})                         # first 3 digits
            (\s|-|\.)                       # separator
            (\d{4})                         # last 4 digits
            (\s*(ext|x|ext.)\s*(\d{2,5}))?  # extension
            )''', re.VERBOSE)

        # Create email regex
        self.email_regex = re.compile(r'''(
            [a-zA-Z0-9._%+-]+   # username
            @                   # @ symbol
            [a-zA-Z0-9.-]+      # domain name
            (\.[a-zA-Z]{2,4})   # dot-something
            )''', re.VERBOSE)

        # Find matches in clipboard text.
        self.clipboard_text = str(pyperclip.paste())
        self.matches = []

        self.init_UI()

    #===========================================
    def init_config(self):
        self.resizable(True, True)
        self.title('Phone Number and Email Address Extractor Version 1.0')
        self.iconbitmap('python.ico')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

    def init_UI(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        label = ttk.Label(self.main_frame, text='** Copy text to the clipboard, and then run program.')
        label.pack(side=tk.TOP, anchor=tk.W)

        self.textbox = st.ScrolledText(self.main_frame, wrap = tk.WORD)
        self.textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.textbox.insert('1.0', self.clipboard_text)
        self.textbox.config(state=tk.DISABLED)

        self.listbox = tk.Listbox(self.main_frame)
        self.listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.listbox.focus()

        for groups in self.phone_regex.findall(self.textbox.get('1.0', tk.END).strip()):
            phone_number = '-'.join([groups[1], groups[3], groups[5]])
            if groups[8] != '':
                phone_number += ' x' + groups[8]
            self.matches.append(phone_number)
        for groups in self.email_regex.findall(self.textbox.get('1.0', tk.END).strip()):
            self.matches.append(groups[0])

        if len(self.matches) > 0:
            pyperclip.copy('\n'.join(self.matches))
            for match in list(self.matches):
                self.listbox.insert(tk.END, match)
        else:
            mb.showerror('Error', 'No phone numbers or email addresses found.')
            self.destroy()

#===========================
# Start GUI
#===========================

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()