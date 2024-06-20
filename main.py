import tkinter as tk
from tkinter import messagebox
import pygame
import time
import threading

# Initialize pygame mixer
pygame.mixer.init()

# Define sound frequencies and durations
DOT_DURATION = 0.2  # Duration of dot
DASH_DURATION = 0.6  # Duration of dash
FREQUENCY = 800  # Frequency in Hz

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
}

# Reverse Morse code dictionary
MORSE_CODE_DICT_REVERSE = {value: key for key, value in MORSE_CODE_DICT.items()}


def string_to_morse_code(input_string):
    """
    Convert a string to Morse code.

    Parameters:
    input_string (str): The input string to be converted.

    Returns:
    str: The Morse code representation of the input string.
    """
    input_string = input_string.upper()
    morse_code = ""

    for char in input_string:
        if char == ' ':
            morse_code += '   '  # Use three spaces to indicate a word separator
        elif char in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[char] + ' '
        else:
            morse_code += '? '  # Indicate an unknown character

    return morse_code.strip()


def morse_code_to_string(morse_code):
    """
    Convert Morse code to a string.

    Parameters:
    morse_code (str): The Morse code to be converted.

    Returns:
    str: The string representation of the Morse code.
    """
    words = morse_code.split('   ')  # Words are separated by three spaces
    decoded_string = []

    for word in words:
        decoded_word = ''
        for code in word.split():
            if code in MORSE_CODE_DICT_REVERSE:
                decoded_word += MORSE_CODE_DICT_REVERSE[code]
            else:
                decoded_word += '?'  # Indicate an unknown Morse code
        decoded_string.append(decoded_word)

    return ' '.join(decoded_string)


def convert_to_morse():
    """
    Convert the input text to Morse code and display the result.
    """
    input_text = input_entry.get()
    if input_text:
        morse_code = string_to_morse_code(input_text)
        result_label.config(text=morse_code)
    else:
        messagebox.showwarning("Input Error", "Please enter text to convert to Morse code.")


def convert_to_text():
    """
    Convert the input Morse code to text and display the result.
    """
    input_text = input_entry.get()
    if input_text:
        text = morse_code_to_string(input_text)
        result_label.config(text=text)
    else:
        messagebox.showwarning("Input Error", "Please enter Morse code to convert to text.")


def clear_text():
    """
    Clear the input field and the result display.
    """
    input_entry.delete(0, tk.END)
    result_label.config(text="")


def copy_to_clipboard():
    """
    Copy the result to the clipboard.
    """
    root.clipboard_clear()
    root.clipboard_append(result_label.cget("text"))
    messagebox.showinfo("Copied", "Result copied to clipboard")


def display_morse_code_dict():
    """
    Display the Morse code dictionary in a new window.
    """
    dict_window = tk.Toplevel(root)
    dict_window.title("Morse Code Dictionary")
    dict_window.geometry("300x400")

    dict_label = tk.Label(dict_window, text="Morse Code Dictionary", font=("Helvetica", 14))
    dict_label.pack(pady=10)

    text_area = tk.Text(dict_window, font=("Helvetica", 12), wrap=tk.WORD)
    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    for key, value in sorted(MORSE_CODE_DICT.items()):
        text_area.insert(tk.END, f"{key}: {value}\n")

    text_area.config(state=tk.DISABLED)


stop_playing = False


def play_morse_sound(morse_code):
    """
    Play sound for the given Morse code.

    Parameters:
    morse_code (str): The Morse code to be played.
    """
    global stop_playing
    for symbol in morse_code:
        if stop_playing:
            break
        if symbol == '.':
            pygame.mixer.Sound('dot.wav').play()
            time.sleep(DOT_DURATION)
        elif symbol == '-':
            pygame.mixer.Sound('dash.wav').play()
            time.sleep(DASH_DURATION)
        elif symbol == ' ':
            time.sleep(DOT_DURATION)  # Space between symbols
        elif symbol == '   ':
            time.sleep(DOT_DURATION * 3)  # Space between words


def play_text_as_morse():
    """
    Play the input text as Morse code sounds.
    """
    global stop_playing
    stop_playing = False
    input_text = input_entry.get()
    if input_text:
        morse_code = string_to_morse_code(input_text)
        threading.Thread(target=play_morse_sound, args=(morse_code,)).start()
    else:
        messagebox.showwarning("Input Error", "Please enter text to play as Morse code.")


def stop_playing_morse():
    """
    Stop playing the Morse code sounds.
    """
    global stop_playing
    stop_playing = True


# Initialize the main window
root = tk.Tk()
root.title("Text to Morse Code Converter")

# Style configurations
root.geometry("500x450")
root.resizable(False, False)
root.config(bg="#f0f0f0")

# Title Label
title_label = tk.Label(root, text="Text and Morse Code Converter", font=("Helvetica", 16), bg="#f0f0f0")
title_label.pack(pady=10)

# Input Field
input_entry = tk.Entry(root, font=("Helvetica", 12), width=40)
input_entry.pack(pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

to_morse_button = tk.Button(button_frame, text="Convert to Morse Code", command=convert_to_morse,
                            font=("Helvetica", 12))
to_morse_button.grid(row=0, column=0, padx=5)

to_text_button = tk.Button(button_frame, text="Convert to Text", command=convert_to_text, font=("Helvetica", 12))
to_text_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_text, font=("Helvetica", 12))
clear_button.grid(row=0, column=2, padx=5)

copy_button = tk.Button(button_frame, text="Copy", command=copy_to_clipboard, font=("Helvetica", 12))
copy_button.grid(row=0, column=3, padx=5)

dict_button = tk.Button(button_frame, text="Show Morse Code Dictionary", command=display_morse_code_dict,
                        font=("Helvetica", 12))
dict_button.grid(row=1, column=0, columnspan=4, pady=10)

play_text_button = tk.Button(button_frame, text="Play Text as Morse", command=play_text_as_morse,
                             font=("Helvetica", 12))
play_text_button.grid(row=2, column=0, columnspan=2, pady=10)

stop_play_button = tk.Button(button_frame, text="Stop Playing", command=stop_playing_morse,
                             font=("Helvetica", 12))
stop_play_button.grid(row=2, column=2, columnspan=2, pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0", wraplength=400, justify="center")
result_label.pack(pady=20)

# Start the main loop
root.mainloop()
