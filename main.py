from tkinter import *
from tkinter import messagebox
import json

MAIN_COLOUR = "#c0f2f6"


def add():
    """ Function to add new entries to data file. """
    station = station_entry.get().title()
    item = item_entry.get().title()
    new_data = {
        station: {
            "items": [item]
        }
    }
    if len(station) == 0:
        messagebox.showerror(title="Error", message="You've left 'Station' field empty!")
    elif len(item) == 0:
        messagebox.showerror(title="Error", message="You've left 'Item' field empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            if station not in data:
                data.update(new_data)
            else:
                data[station]["items"].append(item)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            station_entry.delete(0, "end")
            item_entry.delete(0, "end")
            station_entry.focus()


def find_station():
    """ Function to search for station and display items in this station. """
    station = station_entry.get().title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error!", message="No Data File Found.")
    else:
        if station in data:
            messagebox.showinfo(title=station, message=f"Items at the station: {data[station]['items']}")
        else:
            messagebox.showerror(title="Error!", message=f"No details for {station} exists.")


def find_item():
    """ Function to search for items and display stations with this item. """
    search_item = item_entry.get().title()
    stations_with_item = ""
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error!", message="No Data File Found.")
    else:
        for station, items in data.items():
            for entry, items_list in items.items():
                if search_item in items_list:
                    stations_with_item += station
                    stations_with_item += ", "
        if len(stations_with_item) == 0:
            messagebox.showwarning(title="No data.", message="Item not in data file.")
        else:
            messagebox.showinfo(title=search_item, message=stations_with_item)


""" UI Setup """

window = Tk()
window.title("Items locations.")
window.config(padx=50, pady=50, bg="#c0f2f6")

canvas = Canvas(width=480, height=560, bg=MAIN_COLOUR, highlightthickness=0)
logo_image = PhotoImage(file="logo3.png")
canvas.create_image(248, 290, image=logo_image)
canvas.grid(column=1, row=0)

station_label = Label(text="Station:", bg=MAIN_COLOUR)
station_label.grid(column=0, row=1)
item_label = Label(text="Item Name:", bg=MAIN_COLOUR)
item_label.grid(column=0, row=2)

station_entry = Entry(width=47)
station_entry.grid(column=1, row=1)
station_entry.focus()
item_entry = Entry(width=47)
item_entry.grid(column=1, row=2)

station_search_button = Button(text="Search", width=10,bg=MAIN_COLOUR,highlightthickness=0, command=find_station)
station_search_button.grid(column=2, row=1)
item_search_button = Button(text="Search", width=10, bg=MAIN_COLOUR,highlightthickness=0, command=find_item)
item_search_button.grid(column=2, row=2)
add_button = Button(text="ADD", width=39,bg=MAIN_COLOUR,highlightthickness=0, command=add)
add_button.grid(column=1, row=3)

window.mainloop()
