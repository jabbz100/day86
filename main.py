import tkinter as tk
from tkinter import font, ttk
from PIL import Image, ImageTk
import random
import time


start_time = None
char_count = 0


def restart_window():
    """Reset the WPM score"""
    global start_time
    global char_count
    wpm_label.config(text=f"Words per minute: {0}")
    start_time = None
    char_count = 0
    entry.delete(0, tk.END)


def update_window():
    if start_time:
        elapsed_time = (time.time() - start_time) / 60  # Minutes
        wpm = int(char_count / 5 / elapsed_time) if elapsed_time > 0 else 0
        wpm_label.config(text=f"Words per minute: {wpm}")

    root.after(100, update_window)


# App Setup
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

restart_button = ttk.Button(root, text="Restart", style="TButton", command=restart_window)
restart_button.grid(row=3)

# User Interface Styling
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TEntry",
    font=("Helvetica", 18),
    padding=5,
    borderwidth=2,
    relief="flat",
)
style.map(
    "TEntry",
    background=[("focus", "white")],
    fieldbackground=[("!focus", "#F0F0F0")],
    bordercolor=[("focus", "#0078D7")],
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
    background=[("active", "#67b")],
    foreground=[("active", "#eaeaea")],
)
style.configure(
    "Fancy.TFrame",
    background="#282c34",
    lightcolor="#5a9",
    darkcolor="#1e1e1e"
)

# Typing Panel Layout
typing_panel = ttk.Frame(root, style="Fancy.TFrame")
typing_panel.grid(row=2, pady=30)

wpm_label = tk.Label(typing_panel, text=f"Words per minute: {0}", bg="#282c34", fg="white", font=game_font)
wpm_label.config(font=("Comic Sans MS", 30))
wpm_label.grid(row=0, pady=10)

typing_panel_label = tk.Label(typing_panel, text="", bg="#282c34", fg="white", font=game_font)
typing_panel_label.grid(row=1, pady=10)

entry = ttk.Entry(typing_panel, style="TEntry", font=game_font)
entry.grid(row=2, pady=20, padx=180)


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
    typing_panel_label.config(text=formatted_text)
    return new_words


random_words = update_words()


def check_input(event):
    global random_words

    user_input = entry.get()
    if user_input in random_words:
        new_batch = get_random_words(num_lines=1)[0]
        random_words.remove(user_input)
        random_words.append(new_batch)
        formatted_text = '\n'.join(random_words)
        typing_panel_label.config(text=formatted_text)
        entry.delete(0, tk.END)


def key_press(event):
    global start_time
    global char_count

    if start_time is None:
        start_time = time.time()

    if event.char.isprintable() and event.keysym != "BackSpace":
        user_input = entry.get()
        correct_text = " ".join(random_words)
        if correct_text.startswith(user_input):
            char_count += 1


def combined_handler(event):
    check_input(event)
    key_press(event)


entry.bind("<KeyRelease>", combined_handler)

update_window()

root.mainloop()
