import os
import re
import threading
import itertools
import time
from tkinter import Tk, filedialog

# ---------------- Banner ----------------
print("NFA Extractor — made by GPT\n")

# ---------------- Loading Animation ----------------
loading = True

def spinner():
    for c in itertools.cycle("|/-\\"):
        if not loading:
            break
        print(f"\rProcessing {c}", end="", flush=True)
        time.sleep(0.1)
    print("\rProcessing done.   ")

# ---------------- Clipboard-safe exit ----------------
def copy_and_exit():
    root.clipboard_clear()
    root.clipboard_append(nfatxt)
    root.update_idletasks()
    print("\nCopied to clipboard.")
    print("Exiting in 1 second.....DO.......NOT........CLOSE.....THE.....WINDOW")
    root.after(1000, root.destroy)

# ---------------- Tk setup ----------------
root = Tk()
root.withdraw()

file_path = filedialog.askopenfilename(title="Select a file")

# Final clipboard variable
nfatxt = ""

if not file_path or not os.path.exists(file_path):
    print("File not found.")
    root.destroy()
    exit()

# Start loading animation
spinner_thread = threading.Thread(target=spinner)
spinner_thread.start()

results = []

try:
    with open(file_path, 'rb') as f:
        content = f.read()

    strings = re.findall(b'[\x20-\x7e]{4,}', content)
    filename = os.path.splitext(os.path.basename(file_path))[0]

    for s in strings:
        decoded = s.decode('ascii', errors='ignore')
        if decoded.startswith('eyA'):
            results.append(f"{filename}----{decoded}")

except Exception as e:
    print(f"\nError reading file: {e}")

# Stop loading animation
loading = False
spinner_thread.join()

# Build final text
if results:
    nfatxt = "\n".join(results)

    print("\nFound NFA(s):")
    print(nfatxt)

    copy_and_exit()
    root.mainloop()
else:
    print("\nNo matching NFA strings found.")
    root.destroy()

