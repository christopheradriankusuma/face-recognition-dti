
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1280x720")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    960.0,
    0.0,
    1280.0,
    720.0,
    fill="#3D4B66",
    outline="")

canvas.create_text(
    974.0,
    309.0,
    anchor="nw",
    text="DTI",
    fill="#FFFFFF",
    font=("Inter SemiBold", 48 * -1)
)

canvas.create_text(
    974.0,
    243.0,
    anchor="nw",
    text="Recognition ",
    fill="#FFFFFF",
    font=("Inter SemiBold", 48 * -1)
)

canvas.create_text(
    974.0,
    177.0,
    anchor="nw",
    text="Face",
    fill="#FFFFFF",
    font=("Inter SemiBold", 48 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    # command=lambda: print("button_1 clicked"),
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=1006.0,
    y=480.0,
    width=228.0,
    height=64.0
)
window.resizable(False, False)
window.mainloop()
