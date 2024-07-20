import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import webbrowser

history_file = "history.json"
history_html_file = "history.html"

def load_history():
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            return json.load(file)
    return []

def save_history(data):
    with open(history_file, "w") as file:
        json.dump(data, file)

def generate_history_html():
    history = load_history()
    html_content = "<html><head><title>History</title></head><body>"
    html_content += "<h1>FLAMES History</h1>"
    
    if history:
        for entry in history:
            html_content += f"<p>{entry['name1']} - {entry['name2']}: {entry['relationship']}</p>"
    else:
        html_content += "<p>No history available.</p>"
    
    html_content += '<button onclick="window.location.reload();">Refresh</button>'
    html_content += '<button onclick="window.location.href=\'delete_all_history\'">Delete All</button>'
    html_content += "</body></html>"
    
    with open(history_html_file, "w") as file:
        file.write(html_content)

def open_history_in_browser():
    generate_history_html()
    webbrowser.open(f"file://{os.path.abspath(history_html_file)}")

def delete_all_history():
    if os.path.exists(history_file):
        os.remove(history_file)
    if os.path.exists(history_html_file):
        os.remove(history_html_file)

def flames_game(name1, name2):
    # Clean and prepare the names
    name1 = name1.lower().replace(" ", "")
    name2 = name2.lower().replace(" ", "")
    
    # Calculate the frequency of each character in both names
    freq1 = {}
    freq2 = {}
    
    for char in name1:
        freq1[char] = freq1.get(char, 0) + 1
    for char in name2:
        freq2[char] = freq2.get(char, 0) + 1
    
    # Calculate the number of unique characters
    total_chars = sum(abs(freq1.get(char, 0) - freq2.get(char, 0)) for char in set(name1 + name2))
    
    # FLAMES acronym
    flames = ["Friendship", "Love", "Affection", "Marriage", "Enemies", "Sister"]

    # Determine the relationship
    index = 0
    while len(flames) > 1:
        index = (index + total_chars - 1) % len(flames)
        flames.pop(index)
    
    return flames[0]

def on_calculate():
    name1 = entry1.get()
    name2 = entry2.get()
    if not name1 or not name2:
        messagebox.showerror("Input Error", "Please enter both names.")
        return
    
    relationship = flames_game(name1, name2)
    result_label.config(text=f"Relationship: {relationship}")
    
    # Save to history
    history = load_history()
    history.append({"name1": name1, "name2": name2, "relationship": relationship})
    save_history(history)

def show_history():
    open_history_in_browser()

# Create the main window
root = tk.Tk()
root.title("FLAMES Game")

# Set the window to full screen
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))  # Press ESC to exit full screen

# Load and set the background image
image_path = "C:/Users/LENOVO/projects/flames/flames1.jpeg"
bg_image = Image.open(image_path)

# Update to fit the screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create and place widgets
title_label = tk.Label(root, text="FLAMES Game", font=("Arial", 24, "bold"), fg="white", bg="black")
title_label.pack(pady=20)

frame = tk.Frame(root, bg="black", bd=0)
frame.pack(pady=10)

tk.Label(frame, text="Enter the first name:", font=("Arial", 14), fg="white", bg="black").grid(row=0, column=0, padx=10, pady=10)
tk.Label(frame, text="Enter the second name:", font=("Arial", 14), fg="white", bg="black").grid(row=1, column=0, padx=10, pady=10)

entry1 = tk.Entry(frame, font=("Arial", 14))
entry1.grid(row=0, column=1, padx=10, pady=10)

entry2 = tk.Entry(frame, font=("Arial", 14))
entry2.grid(row=1, column=1, padx=10, pady=10)

calculate_button = tk.Button(root, text="Calculate Relationship", command=on_calculate, font=("Arial", 14), fg="black", bg="white")
calculate_button.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="white", bg="black")
result_label.pack(pady=10)

# History Button
history_button = tk.Button(root, text="History", command=show_history, font=("Arial", 14), fg="black", bg="white")
history_button.pack(side=tk.LEFT, padx=10, pady=10)

# License Stamp
license_label = tk.Label(root, text="© 2024 Your License Info", font=("Arial", 10), fg="white", bg="black")
license_label.pack(side=tk.BOTTOM, pady=10)

# Start the main loop
root.mainloop()
