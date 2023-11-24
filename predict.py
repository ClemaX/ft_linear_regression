#!/usr/bin/env python

from sys import stderr

from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from common import *


lines = []


def model_plot():
    return ax.axline((0, params['theta'][0]), slope=params['theta'][1], color='#50fa7b')


def prediction_plot(x, y):
    ax.set_xlim(x - 3, x + 3)

    return ax.plot(x, y, 'ro')


def predict(*args):
    global lines

    try:
        mileage = float(mileage_str.get())
        if mileage < 0:
            raise ValueError(mileage)
    except ValueError:
        pass
    else:
        standardized_mileage = (mileage - params['mileage_mean'][0]) / params['mileage_std'][0]

        price = max(0, model(params, standardized_mileage))

        price_str.set(round(price, 2))

        for line in lines:
            line.remove()

        lines = prediction_plot(standardized_mileage, price)

        canvas.draw()


# Load trained params
try:
    params = params_load()
except FileNotFoundError:
    print("Parameters file does not exist! Please run train.py first.", file=stderr)
    exit(1)

# Initialize Tk root
root = Tk()
root.title("Car Price Prediction")

# Configure TTK styles
style = ttk.Style(root)
style_entry = ttk.Style()

style.configure('.', background='#1e1f28', fieldbackground='black', foreground='#f8f8f2')
style_entry.configure('style.TEntry', fieldbackground='black', foreground='#f8f8f2')

# Configure root and frame layout
main_frame = ttk.Frame(root, padding="3 3 12 12")
main_frame.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Initialize matplotlib figure and axes
fig = Figure(figsize=(7, 5), dpi=100)

ax = fig.add_subplot(title="Car Price Prediction")

ax.set_xlabel("Mileage")
ax.set_ylabel("Price")

ax.set_xlim(-3, 3)
ax.set_ylim(0, 15000)

# Plot trained model
model_plot()

# Add Tk FigureCanvas
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.draw()

# Add Tk NavigationToolbar
toolbar = NavigationToolbar2Tk(canvas, main_frame, pack_toolbar=False)
toolbar.update()

# Layout canvas and toolbar
canvas.get_tk_widget().grid(column=1, row=1, rowspan=3, sticky=(S, W, E))
toolbar.grid(column=1, row=4, sticky=(W, E))

# Initialize view-model
mileage_str = StringVar()
price_str = StringVar()

# Add mileage input
mileage_entry = ttk.Entry(main_frame, style='style.TEntry', width=8, textvariable=mileage_str)
mileage_entry.grid(column=2, row=1, sticky=(W, E))
ttk.Label(main_frame, text="kms").grid(column=3, row=1, sticky=(W))

# Add price prediction
ttk.Label(main_frame, textvariable=price_str).grid(column=2, row=2, sticky=(W, E))
ttk.Label(main_frame, text="$").grid(column=3, row=2, sticky=(W))

# Add price prediction button3
ttk.Button(main_frame, text="Predict", command=predict).grid(column=3, row=3, sticky=(W))

for child in main_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

mileage_entry.focus()

root.bind("<Return>", predict)

mainloop()
