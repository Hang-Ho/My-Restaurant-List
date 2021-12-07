from tkinter import *
import sqlite3
import pandas as pd
from pandastable import Table
import testdata

root = Tk()
root.title('My Restaurant List')
root.geometry("400x400")
root.configure(bg='light blue')

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS ratingTB;""")
cursor.execute("""DROP TABLE IF EXISTS cuisineTB;""")
cursor.execute("""DROP TABLE IF EXISTS restaurantTB;""")

connection.commit()
connection.close()

testdata.create_tables()
testdata.insert_values()


# Add new restaurant to database
def add_res():
    clear_window()

    # Text boxes and labels
    name = Entry(root, width=30)
    name.grid(row=0, column=1, padx=20)
    name_label = Label(root, text="Restaurant name:", bg="light blue")
    name_label.grid(row=0, column=0)

    street_address = Entry(root, width=30)
    street_address.grid(row=1, column=1)
    street_address_label = Label(root, text="Street address:", bg="light blue")
    street_address_label.grid(row=1, column=0)

    city = Entry(root, width=30)
    city.grid(row=2, column=1, padx=20)
    city_label = Label(root, text="City:", bg="light blue")
    city_label.grid(row=2, column=0)

    state = Entry(root, width=30)
    state.grid(row=3, column=1, padx=20)
    state_label = Label(root, text="State:", bg="light blue")
    state_label.grid(row=3, column=0)

    zipcode = Entry(root, width=30)
    zipcode.grid(row=4, column=1, padx=20)
    zipcode_label = Label(root, text="Zip code:", bg="light blue")
    zipcode_label.grid(row=4, column=0)

    cuisine = Entry(root, width=30)
    cuisine.grid(row=5, column=1)
    cuisine_label = Label(root, text="Cuisine (separate by comma):", bg="light blue")
    cuisine_label.grid(row=5, column=0)

    curbside_pickup = StringVar(value='no')
    delivery = StringVar(value='no')

    curbside_pickup_label = Label(root, text="Curbside pickup:", bg="light blue")
    curbside_pickup_label.grid(row=6, column=0)

    rb1 = Radiobutton(root, text="Yes", variable=curbside_pickup, value='yes', bg="light blue")
    rb1.grid(row=7, column=0)
    rb2 = Radiobutton(root, text="No", variable=curbside_pickup, value="no", bg="light blue")
    rb2.grid(row=7, column=1)

    delivery_label = Label(root, text="Delivery:", bg="light blue")
    delivery_label.grid(row=8, column=0)

    rb3 = Radiobutton(root, text="Yes", variable=delivery, value="yes", bg="light blue")
    rb3.grid(row=9, column=0)
    rb4 = Radiobutton(root, text="No", variable=delivery, value="no", bg="light blue")
    rb4.grid(row=9, column=1)

    submit_add_res_btn = Button(root, text="Submit", bg="pink", fg="black",
                                command=lambda: submit_add_res(name.get().strip(), street_address.get().strip(),
                                                               city.get().strip(), state.get().strip(),
                                                               zipcode.get().strip(),
                                                               curbside_pickup.get(), delivery.get(), cuisine.get()))
    submit_add_res_btn.grid(row=11, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

    display_exit(11)


# Handle submit add new restaurant
def submit_add_res(name, street_address, city, state, zipcode, curbside_pickup, delivery, cuisine):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    text = StringVar()

    # Check if restaurant is in list or not
    if any(name in res for res in get_res()):
        text.set(f"{name} is already in the restaurant list!")
    elif name == '' or street_address == '' or city == '' or state == '' \
            or zipcode == '' or curbside_pickup == '' \
            or delivery == '' or cuisine == '':
        text.set("Please fill up all information of the restaurant you want to add.")
    else:
        cur.execute(
            "INSERT INTO restaurantTB (name, street_address, city, state, zipcode, curbside_pickup, delivery)"
            "VALUES (:name, :street_address, :city, :state, :zipcode, :curbside_pickup, :delivery);",
            {'name': name,
             'street_address': street_address,
             'city': city,
             'state': state,
             'zipcode': zipcode,
             'curbside_pickup': curbside_pickup,
             'delivery': delivery
             })
        for cui in cuisine.split(","):
            cur.execute("INSERT INTO cuisineTB (cuisine, restaurant)"
                        " VALUES (:cuisine, :restaurant);",
                        {
                            'cuisine': cui.strip(),
                            'restaurant': name
                        })
        text.set(f"Successfully added {name} to the restaurant list!")

    clear_window()
    return_btn()

    label = Label(root, text=text.get(), bg="light blue")
    label.grid(row=3, column=0, columnspan=3)

    con.commit()
    con.close()


# Add rating to rating table
def add_rating():
    clear_window()

    # Test boxes and labels
    name = Entry(root, width=30)
    name.grid(row=0, column=1, padx=20)
    rating = Entry(root, width=30)
    rating.grid(row=1, column=1)

    name_label = Label(root, text="Restaurant name:", bg="light blue")
    name_label.grid(row=0, column=0)
    rating_label = Label(root, text="Enter your rating score (1-5):", bg="light blue")
    rating_label.grid(row=1, column=0)

    submit_add_rating_btn = Button(root, text="Submit", bg="pink", fg="black",
                                   command=lambda: submit_add_rating(name.get().strip(), rating.get()))
    submit_add_rating_btn.grid(row=3, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

    display_exit(3)


# Handle submit add rating
def submit_add_rating(name, rating):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    text = StringVar()

    # Check if restaurant is in list or not
    if name == '' or rating == '':
        text.set("Please fill up all entry boxes.")
    elif any(name in res for res in get_res()):
        cur.execute("INSERT INTO ratingTB (restaurant, rating) VALUES (:name, :rating);",
                    {'name': name,
                     'rating': int(rating)
                     })
        text.set("Successfully added rating. Thank you for your feedback!")
    else:
        text.set(f"Sorry, {name} has not yet in the database.")

    clear_window()
    return_btn()

    label = Label(root, text=text.get(), bg="light blue")
    label.grid(row=2, column=0, columnspan=3)

    con.commit()
    con.close()


# Handle view all restaurant in list
def see_all_res():
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    cur.execute("SELECT name, cuisine, street_address, city, state, zipcode"
                " FROM restaurantTB LEFT JOIN cuisineTB"
                " ON restaurantTB.name = cuisineTB.restaurant"
                " GROUP BY name;")

    display_result(cur.fetchall())

    con.commit()
    con.close()


# Function find restaurant by name
def find_res_by_name():
    clear_window()

    # Get restaurant name
    name = Entry(root, width=30)
    name.grid(row=0, column=1, padx=20)

    name_label = Label(root, text="Enter restaurant name:", bg="light blue")
    name_label.grid(row=0, column=0)

    submit_find_res_by_name_btn = Button(root, text="Submit", bg="pink", fg="black",
                                         command=lambda: submit_find_res_by_name(name))
    submit_find_res_by_name_btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

    display_exit(1)


# Handle submit find restaurant by name
def submit_find_res_by_name(name):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    # Check empty string
    if name.get().strip() == '':
        clear_window()
        return_btn()
        text = StringVar()
        text.set("Please enter restaurant name!")
        label = Label(root, text=text.get(), bg="light blue")
        label.grid(row=2, column=0, columnspan=2)
    else:
        cur.execute("SELECT name, cuisine, street_address, city, state, zipcode"
                    " FROM restaurantTB LEFT JOIN cuisineTB"
                    " ON restaurantTB.name = cuisineTB.restaurant"
                    " WHERE name = :name GROUP BY name;",
                    {'name': name.get().strip()})
        name.delete(0, END)
        display_result(cur.fetchall())

    con.commit()
    con.close()


# Function find restaurant by cuisine
def find_res_by_cuisine():
    clear_window()

    # Get cuisine
    cuisine = Entry(root, width=30)
    cuisine.grid(row=0, column=1, padx=20)

    cuisine_label = Label(root, text="Enter cuisine:", bg="light blue")
    cuisine_label.grid(row=0, column=0)

    submit_find_res_by_cuisine_btn = Button(root, text="Submit", bg="pink", fg="black",
                                            command=lambda: submit_find_res_by_cuisine(cuisine))
    submit_find_res_by_cuisine_btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

    display_exit(1)


# Handle submit find restaurant by cuisine
def submit_find_res_by_cuisine(cuisine):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    if cuisine.get().strip() == '':
        clear_window()
        return_btn()
        text = StringVar()
        text.set("Please enter restaurant cuisine!")
        label = Label(root, text=text.get(), bg="light blue")
        label.grid(row=2, column=0, columnspan=2)
    else:
        cur.execute("SELECT name, street_address, city, state, zipcode"
                    " FROM restaurantTB, cuisineTB"
                    " WHERE restaurantTB.name = cuisineTB.restaurant"
                    " AND cuisineTB.cuisine = :cuisine GROUP BY name;",
                    {'cuisine': cuisine.get().strip()})

        cuisine.delete(0, END)

        records = cur.fetchall()

        data = {
            'Name': [],
            'Address': []
        }
        for record in records:
            data['Name'].append(record[0])
            data['Address'].append(record[1] + ', ' + record[2] + ', ' + record[3] + ', ' + record[4])
        if len(records) == 0:
            display_no_result()
        else:
            df = pd.DataFrame(data)
            display_popup(df)

    con.commit()
    con.close()


# Function find restaurant by zip code
def find_res_by_zipcode():
    clear_window()

    # Get zip code
    zipcode = Entry(root, width=30)
    zipcode.grid(row=0, column=1, padx=20)

    zipcode_label = Label(root, text="Enter your zipcode:", bg="light blue")
    zipcode_label.grid(row=0, column=0)

    submit_find_res_by_zipcode_btn = Button(root, text="Submit", bg="pink", fg="black",
                                            command=lambda: submit_find_res_by_zipcode(zipcode))
    submit_find_res_by_zipcode_btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

    display_exit(1)


# Handle submit find restaurant by zip code
def submit_find_res_by_zipcode(zipcode):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    if zipcode.get().strip() == '':
        clear_window()
        return_btn()
        text = StringVar()
        text.set("Please enter zipcode!")
        label = Label(root, text=text.get(), bg="light blue")
        label.grid(row=2, column=0, columnspan=2)
    else:
        cur.execute("SELECT name, cuisine, street_address, city"
                    " FROM restaurantTB, cuisineTB"
                    " WHERE restaurantTB.name = cuisineTB.restaurant"
                    " AND restaurantTB.zipcode = :zipcode GROUP BY name;",
                    {'zipcode': zipcode.get().strip()})

        zipcode.delete(0, END)

        records = cur.fetchall()

        data = {
            'Name': [],
            'Cuisine': [],
            'Address': []
        }
        for record in records:
            data['Name'].append(record[0])
            data['Cuisine'].append(record[1])
            data['Address'].append(record[2] + ', ' + record[3])
        if len(records) == 0:
            display_no_result()
        else:
            df = pd.DataFrame(data)
            display_popup(df)

    con.commit()
    con.close()


# Function find best restaurant(s) with limit number
def find_best_res():
    clear_window()

    # Get limit number
    limit = Entry(root, width=7)
    limit.grid(row=0, column=2)

    limit_label = Label(root, text="How many restaurant would you like to view?", bg="light blue")
    limit_label.grid(row=0, column=0, columnspan=2)

    submit_find_best_res_btn = Button(root, text="Submit", bg="pink", fg="black",
                                      command=lambda: submit_find_best_res(limit))
    submit_find_best_res_btn.grid(row=2, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

    display_exit(2)


# Handle submit find best restaurant
def submit_find_best_res(limit):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    if limit.get().strip() == '':
        clear_window()
        return_btn()
        text = StringVar()
        text.set("Please enter the number of restaurant you want to view!")
        label = Label(root, text=text.get(), bg="light blue")
        label.grid(row=2, column=0, columnspan=3)
    else:
        cur.execute("SELECT name, cuisine, street_address, city, state, zipcode, AVG(rating)"
                    " FROM restaurantTB, ratingTB, cuisineTB"
                    " WHERE restaurantTB.name = ratingTB.restaurant"
                    " GROUP BY name"
                    " ORDER BY AVG(rating)"
                    " DESC LIMIT :limit;",
                    {'limit': limit.get().strip()})

        limit.delete(0, END)

        records = cur.fetchall()

        data = {
            'Name': [],
            'Cuisine': [],
            'Address': [],
            'Rating': []
        }
        for record in records:
            data['Name'].append(record[0])
            data['Cuisine'].append(record[1])
            data['Address'].append(record[2] + ', ' + record[3] + ', ' + record[4] + ', ' + record[5])
            data['Rating'].append(record[6])
        if len(records) == 0:
            display_no_result()
        else:
            df = pd.DataFrame(data)
            display_popup(df)

    con.commit()
    con.close()


# Function fin restaurants have delivery service
def find_delivery_res():
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    cur.execute("SELECT name, cuisine"
                " FROM restaurantTB, cuisineTB"
                " WHERE restaurantTB.name = cuisineTB.restaurant"
                " AND restaurantTB.delivery = 'yes'"
                " GROUP BY name;")
    records = cur.fetchall()

    data = {
        'Name': [],
        'Cuisine': []
    }
    for record in records:
        data['Name'].append(record[0])
        data['Cuisine'].append(record[1])
    if len(records) == 0:
        display_no_result()
    else:
        df = pd.DataFrame(data)
        display_popup(df)

    con.commit()
    con.close()


# Function find restaurants have curbside pickup
def find_curb_pickup_res():
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    cur.execute("SELECT name, street_address, city, state, zipcode"
                " FROM restaurantTB"
                " WHERE restaurantTB.curbside_pickup='yes'"
                " GROUP BY name;")
    records = cur.fetchall()

    data = {
        'Name': [],
        'Address': []
    }
    for record in records:
        data['Name'].append(record[0])
        data['Address'].append(record[1] + ', ' + record[2] + ', ' + record[3] + ', ' + record[4])
    if len(records) == 0:
        display_no_result()
    else:
        df = pd.DataFrame(data)
        display_popup(df)

    con.commit()
    con.close()


# Function remove restaurant form list
def remove_res():
    clear_window()

    # Get restaurant name to remove
    name = Entry(root, width=30)
    name.grid(row=0, column=1, padx=20)

    name_label = Label(root, text="Restaurant name:", bg="light blue")
    name_label.grid(row=0, column=0)

    submit_remove_res_btn = Button(root, text="Submit", bg="pink", fg="black",
                                   command=lambda: submit_remove_res(name.get().strip()))
    submit_remove_res_btn.grid(row=1, column=0, columnspan=1, pady=10, padx=10, ipadx=50)

    display_exit(1)


# Handle submit remove restaurant by name
def submit_remove_res(name):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    text = StringVar()
    if name == '':
        text.set("Please enter restaurant name!")
    elif any(name in res for res in get_res()):
        cur.execute("DELETE FROM restaurantTB"
                    " WHERE name = :name;",
                    {'name': name})
        text.set(f"Successfully removed {name} from the restaurant list!")
    else:
        text.set(f"{name} has not yet in the restaurant list.")

    clear_window()
    return_btn()

    label = Label(root, text=text.get(), bg="light blue")
    label.grid(row=2, column=0, columnspan=2)

    con.commit()
    con.close()


# Helper function to get all restaurant names to check if a restaurant exists in list
def get_res():
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    cur.execute("SELECT name FROM restaurantTB;")
    records = cur.fetchall()

    con.commit()
    con.close()
    return records


def exit_window():
    root.destroy()


# Main menu
def display_menu():
    add_res_btn = Button(root, text="Add new restaurant", bg="pink", fg="black", command=add_res)
    add_res_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=130)

    add_rating_btn = Button(root, text="Rate a restaurant", bg="pink", fg="black", command=add_rating)
    add_rating_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

    see_all_res_btn = Button(root, text="See all restaurants", bg="pink", fg="black", command=see_all_res)
    see_all_res_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=133)

    find_res_btn = Button(root, text="Find restaurants", bg="pink", fg="black", command=display_find_menu)
    find_res_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

    view_delivery_res_btn = Button(root, text="View restaurants have delivery service", bg="pink", fg="black",
                                   command=find_delivery_res)
    view_delivery_res_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=80)

    view_curb_pickup_res_btn = Button(root, text="View restaurants have curbside pickup", bg="pink", fg="black",
                                      command=find_curb_pickup_res)
    view_curb_pickup_res_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=75)

    remove_res_btn = Button(root, text="Remove restaurant from list", bg="pink", fg="black", command=remove_res)
    remove_res_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=104)

    exit_btn = Button(root, text="Exit", bg="pink", fg="black", command=exit_window)
    exit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=165)


def display_find_menu():
    clear_window()
    return_btn()

    find_res_by_name_btn = Button(root, text="Find restaurants by name", bg="pink", fg="black",
                                  command=find_res_by_name)
    find_res_by_name_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=113)

    find_res_by_cuisine_btn = Button(root, text="Find restaurants by cuisine", bg="pink", fg="black",
                                     command=find_res_by_cuisine)
    find_res_by_cuisine_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=110)

    find_res_by_zipcode_btn = Button(root, text="Find near by restaurants", bg="pink", fg="black",
                                     command=find_res_by_zipcode)
    find_res_by_zipcode_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=115)

    find_best_res_btn = Button(root, text="Find the best restaurant", bg="pink", fg="black", command=find_best_res)
    find_best_res_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=115)


# Helper function to display result
def display_result(records):
    data = {
        'Name': [],
        'Cuisine': [],
        'Address': []
    }
    for record in records:
        data['Name'].append(record[0])
        data['Cuisine'].append(record[1])
        data['Address'].append(record[2] + ', ' + record[3] + ', ' + record[4] + ', ' + record[5])
    if len(records) == 0:
        display_no_result()
    else:
        df = pd.DataFrame(data)
        display_popup(df)


# Show empty result
def display_no_result():
    clear_window()
    return_btn()
    display_label = Label(root, text="No result found", bg="light blue")
    display_label.grid(row=2, column=0, columnspan=2)


# Helper function to display database result in table
def display_popup(df):
    frame = Toplevel(root)
    pt = Table(frame)
    pt.model.df = df
    pt.show()


# Helper function clear window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# Helper function show exit button
def display_exit(row):
    exit_btn = Button(root, text="Exit", bg="pink", fg="black",
                      command=lambda: handle_exit())
    exit_btn.grid(row=row, column=1, columnspan=1, pady=10, padx=10, ipadx=50)


def handle_exit():
    clear_window()
    display_menu()


# Helper function show return button
def return_btn():
    exit_btn = Button(root, text="Return", bg="pink", fg="black",
                      command=lambda: handle_exit())
    exit_btn.grid(row=0, column=1, columnspan=2, pady=10, padx=10, ipadx=162)


display_menu()

root.mainloop()
