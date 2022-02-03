from tkinter import *
import pandas as pd
import random
import os

BACKGROUND_COLOR = "#B1DDC6"

rand_choice = {}

to_learn = {}

countdown_timer = None
# ---------------------------- READING THE CSV AND CONVERITNG IT TO A DICTIONARY DATAFRAME ------------------------------ #
try:
    df = pd.read_csv("data/new_file.csv")
except FileNotFoundError:
    df = pd.read_csv("data/french_words.csv")
    data = pd.DataFrame.to_dict(df, orient="records")
else:
    data = pd.DataFrame.to_dict(df, orient="records")

to_learn = data
# ---------------------------- REVEAL CARDS AFTER DELAY ------------------------------- #


def count_down():
    canvas.itemconfig(front_img, image=card_back_image)
    canvas.itemconfig(title, fill='white', text="English")
    canvas.itemconfig(word, fill='white', text=rand_choice["English"])
# ---------------------------- GENERATING RANDOM WORDS ------------------------------- #


def generate_words():
    global rand_choice, countdown_timer
    rand_choice = random.choice(to_learn)
    canvas.itemconfig(front_img, image=card_front_image)
    canvas.itemconfig(title, fill='black', text="French")
    canvas.itemconfig(word, fill='black', text=rand_choice["French"])
    countdown_timer = window.after(3000, count_down)
# ---------------------------- KNOWN WORDS ------------------------------- #


def known_words():
    global rand_choice
    window.after_cancel(countdown_timer)
    if (len(to_learn)) > 1:
        to_learn.remove(rand_choice)
        new_df = pd.DataFrame(to_learn)
        new_df.to_csv("data/new_file.csv", index=False)
        generate_words()
    else:
        canvas.itemconfig(title, fill='black', text="You reached the end.")
        canvas.itemconfig(word, fill='black', text="GAME OVER")
# ---------------------------- UNKNOWN WORDS ------------------------------- #


def unknown_words():
    global rand_choice
    window.after_cancel(countdown_timer)
    if (len(to_learn)) > 1:
        generate_words()
    else:
        canvas.itemconfig(title, fill='black', text="You reached the end.")
        canvas.itemconfig(word, fill='black', text="GAME OVER")


# ---------------------------- ALL THE IMAGE VARIABLAES ------------------------------- #
window = Tk()

card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")

right_image = PhotoImage(file="images/right.png")
cross_image = PhotoImage(file="images/wrong.png")
# ---------------------------- UI SETUP ------------------------------- #
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=526,
                bg=BACKGROUND_COLOR, highlightthickness=0)

front_img = canvas.create_image(400, 263, image=card_front_image)
title = canvas.create_text(400, 150, text="Title",
                           font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

button1 = Button(image=right_image, highlightthickness=0, command=known_words)
button1.grid(column=1, row=1)

button2 = Button(image=cross_image, highlightthickness=0,
                 command=unknown_words)
button2.grid(column=0, row=1)

# start the program only if data is available
if (len(to_learn)) > 1:
    generate_words()
else:
    canvas.itemconfig(front_img, image=card_front_image)
    canvas.itemconfig(title, fill='black', text="NO Data Found RESTART TO")
    canvas.itemconfig(word, fill='black', text="LEARN AGAIN")
    os.remove("data/new_file.csv")

window.mainloop()
