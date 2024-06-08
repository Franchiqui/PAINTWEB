import time
from tkinter import *
import tkinter as tk
from tkinter import filedialog, simpledialog, font, ttk
from tkinter import colorchooser, messagebox
from PIL import Image, ImageTk, ImageGrab, ImageOps
import io

window = Tk()
window.title("Drawing App")

def select_brush():
    global selected_color
    selected_color = previous_color

def change_brush_size(value):
    global brush_size
    brush_size = int(value)

def select_brush_size():
    new_window = Toplevel(window)
    new_window.title("Select Brush Size")
    new_window.geometry("400x100")

    brush_size_label = Label(new_window, text="Brush Size")
    brush_size_label.pack()

    brush_size_slider = Scale(new_window, from_=1, to=25, orient=HORIZONTAL, command=change_brush_size)
    brush_size_slider.set(brush_size)
    brush_size_slider.pack()

def select_eraser():
    global selected_color, previous_color
    previous_color = selected_color
    selected_color = background_color

def select_eraser_size():
    new_window = Toplevel(window)
    new_window.title("Select Eraser Size")
    new_window.geometry("400x100")

    eraser_size_label = Label(new_window, text="Eraser Size")
    eraser_size_label.pack()

    eraser_size_slider = Scale(new_window, from_=1, to=20, orient=HORIZONTAL, command=change_brush_size)
    eraser_size_slider.set(brush_size)
    eraser_size_slider.pack()

def select_brush_color():
    global selected_color, previous_color
    color = colorchooser.askcolor(title="Select Color")[1]
    if color:
        selected_color = color
        previous_color = color

def select_background_color():
    global background_color, canvas
    color = colorchooser.askcolor(title="Select Color")[1]
    if color:
        background_color = color
        canvas.config(bg=background_color)

def clear_canvas():
    canvas.delete("all")

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        ps = canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img = ImageOps.expand(img, border=(5, 5, 5, 5), fill='white')
        img.save(file_path)

# Default Values
is_drawing = False
last_x = 0
last_y = 0
start_x = 0
start_y = 0
shape = "freehand"
brush_size = 2
selected_color = "black"
previous_color = "black"
background_color = "white"
fill_color = None
image_refs = []
current_object = None

def start_drawing(event):
    global is_drawing, last_x, last_y, start_x, start_y
    is_drawing = True
    last_x, last_y = event.x, event.y
    start_x, start_y = event.x, event.y

    if shape == "text":
        text = simpledialog.askstring("Input", "Enter the text:")
        if text:
            size = simpledialog.askinteger("Input", "Enter text size:", initialvalue=20)
            font_family = font_var.get()
            color = colorchooser.askcolor(title="Select Text Color")[1]
            if color:
                canvas.create_text(start_x, start_y, text=text, fill=color, font=(font_family, size), tags="movable")
    elif shape == "image":
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((100, 100))
            img = ImageTk.PhotoImage(image)
            canvas.create_image(start_x, start_y, image=img, anchor=tk.NW, tags="movable")
            image_refs.append(img)  # Keep reference to avoid garbage collection

def draw(event):
    global is_drawing, last_x, last_y, shape, start_x, start_y, current_object
    if is_drawing:
        x, y = event.x, event.y
        if shape == "freehand":
            canvas.create_line(last_x, last_y, x, y, width=brush_size, fill=selected_color)
            last_x, last_y = x, y
        elif shape in ["line", "rectangle", "circle"]:
            if current_object:
                canvas.delete(current_object)
            if shape == "line":
                current_object = canvas.create_line(start_x, start_y, x, y, width=brush_size, fill=selected_color)
            elif shape == "rectangle":
                current_object = canvas.create_rectangle(start_x, start_y, x, y, outline=selected_color, width=brush_size, fill=fill_color)
            elif shape == "circle":
                current_object = canvas.create_oval(start_x, start_y, x, y, outline=selected_color, width=brush_size, fill=fill_color)

def stop_drawing(event):
    global is_drawing, shape, current_object
    is_drawing = False
    current_object = None

def erase_drawing():
    global selected_color
    selected_color = "white"

def set_shape(new_shape):
    global shape
    shape = new_shape

def set_fill_color():
    global fill_color
    color = colorchooser.askcolor(title="Select Fill Color")[1]
    if color:
        fill_color = color

def add_image():
    global shape
    shape = "image"

def enable_movement(event):
    global current_object
    current_object = event.widget.find_closest(event.x, event.y)
    canvas.tag_raise(current_object)

def move_object(event):
    global current_object
    x, y = event.x, event.y
    canvas.coords(current_object, x, y)

def disable_movement(event):
    global current_object
    current_object = None

# Create the menu bar
menu_bar = Menu(window)

# Create the brush menu
brush_menu = Menu(menu_bar, tearoff=0)
brush_menu.add_command(label="Select Brush", command=select_brush)
brush_menu.add_command(label="Select Brush Size", command=select_brush_size)
brush_menu.add_command(label="Freehand", command=lambda: set_shape("freehand"))
brush_menu.add_command(label="Line", command=lambda: set_shape("line"))
brush_menu.add_command(label="Rectangle", command=lambda: set_shape("rectangle"))
brush_menu.add_command(label="Circle", command=lambda: set_shape("circle"))
brush_menu.add_command(label="Text", command=lambda: set_shape("text"))
brush_menu.add_command(label="Select Fill Color", command=set_fill_color)

# Create the eraser menu
eraser_menu = Menu(menu_bar, tearoff=0)
eraser_menu.add_command(label="Select Eraser", command=select_eraser)
eraser_menu.add_command(label="Select Eraser Size", command=select_eraser_size)

# Create the color menu
color_menu = Menu(menu_bar, tearoff=0)
color_menu.add_command(label="Select Drawing Color", command=select_brush_color)
color_menu.add_command(label="Select Background Color", command=select_background_color)

# Create the clear menu
clear_menu = Menu(menu_bar, tearoff=0)
clear_menu.add_command(label="Clear Canvas", command=clear_canvas)

# Create the save menu
save_menu = Menu(menu_bar, tearoff=0)
save_menu.add_command(label="Save Drawing", command=save_image)

# Create the image menu
image_menu = Menu(menu_bar, tearoff=0)
image_menu.add_command(label="Add Image", command=add_image)

# Add the menus to the menu bar
menu_bar.add_cascade(label="Brush", menu=brush_menu)
menu_bar.add_cascade(label="Eraser", menu=eraser_menu)
menu_bar.add_cascade(label="Color", menu=color_menu)
menu_bar.add_cascade(label="Clear", menu=clear_menu)
menu_bar.add_cascade(label="Save", menu=save_menu)
menu_bar.add_cascade(label="Image", menu=image_menu)

# Configure the menu bar
window.config(menu=menu_bar)

# Add font selection dropdown
font_var = StringVar()
fonts = list(font.families())
font_dropdown = ttk.Combobox(window, textvariable=font_var)
font_dropdown['values'] = fonts
font_dropdown.set(fonts[0])
font_dropdown.pack()

canvas = Canvas(window, width=800, height=480, bg="white")
canvas.pack()

canvas.bind('<Button-1>', start_drawing)
canvas.bind('<B1-Motion>', draw)
canvas.bind('<ButtonRelease-1>', stop_drawing)

# Bind for movement
canvas.tag_bind("movable", "<ButtonPress-1>", enable_movement)
canvas.tag_bind("movable", "<B1-Motion>", move_object)
canvas.tag_bind("movable", "<ButtonRelease-1>", disable_movement)

window.mainloop()
