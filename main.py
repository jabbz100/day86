import tkinter as tk
from tkinter import font, ttk
from PIL import Image, ImageTk
import random
import time


def load_words():
    with open("./data/google-10000-english-usa-no-swears-long.txt", "r") as file:
        words = file.read().splitlines()
    return words


def get_random_words(num_lines=3, words_per_line=3):
    words = load_words()
    selected_words = random.sample(words, num_lines * words_per_line)
    return [' '.join(selected_words[i:i+words_per_line]) for i in range(0, len(selected_words), words_per_line)]


def update_words():
    new_words = get_random_words()
    formatted_text = '\n'.join(new_words)
    game_label.config(text=formatted_text)
    return new_words


def restart_typing():
    pass


# TODO 1. Setup the root window
root = tk.Tk()
root.title("Super Typer")
root.geometry("1280x800")
root.config(bg="#6E8E59")

default_bg = root.cget('bg')

game_font = font.Font(family="Comic Sans MS", size=20)

im_logo = Image.open("data/logo.png")
img_logo = ImageTk.PhotoImage(image=im_logo)

root.columnconfigure(0, weight=1)

logo_label = tk.Label(root, image=img_logo, anchor="center", bg=default_bg)
logo_label.grid(row=0)

tk.Label(root,
         text="Let's see how much of a super typer you are 😊!",
         font=game_font,
         bg=default_bg,
         fg="white",).grid(row=1, pady=10)

# Todo 3. Some Style
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TEntry",
    font=("Helvetica", 18),  # Set a modern font and size
    padding=5,               # Add padding for better aesthetics
    borderwidth=2,           # Slightly thicker border
    relief="flat",           # Flat appearance
)
style.map(
    "TEntry",
    background=[("focus", "white")],  # White background on focus
    fieldbackground=[("!focus", "#F0F0F0")],  # Light gray when not focused
    bordercolor=[("focus", "#0078D7")],  # Highlighted border on focus
)
style.configure(
    "TButton",
    foreground="#ffffff",
    background="#5a9",
    font=("Comic Sans MS", 14, "bold"),
    padding=10,

)
style.map(
    "TButton",
    background=[("active", "#67b")],  # Button hover color
    foreground=[("active", "#eaeaea")],  # Hover text color
)
style.configure(
    "Fancy.TFrame",
    background="#282c34",  # Frame background color
    lightcolor="#5a9",     # Top/left border color for a subtle 3D effect
    darkcolor="#1e1e1e"    # Bottom/right border color
)

restart_button = ttk.Button(root, text="Restart", style="TButton", command=restart_typing)
restart_button.grid(row=3)

# TODO 2. Setup the game box
game_box = ttk.Frame(root, style="Fancy.TFrame")
game_box.grid(row=2, pady=30)

wpm_label = tk.Label(game_box, text=f"Words per minute: {0}", bg="#282c34", fg="white", font=game_font)
wpm_label.config(font=("Comic Sans MS", 30))
wpm_label.grid(row=0, padx=150, pady=10)

game_label = tk.Label(game_box, text="", bg="#282c34", fg="white", font=game_font)
game_label.grid(row=1, pady=10)

entry = ttk.Entry(game_box, style="TEntry", font=game_font)
entry.grid(row=2, pady=20)

random_words = update_words()


def check_input(event=None):
    global random_words
    user_input = entry.get()
    if user_input in random_words:
        new_batch = get_random_words(num_lines=1, words_per_line=3)[0]
        random_words.remove(user_input)
        random_words.append(new_batch)
        formatted_text = '\n'.join(random_words)
        game_label.config(text=formatted_text)
        entry.delete(0, tk.END)


entry.bind("<KeyRelease>", check_input)

root.mainloop()
