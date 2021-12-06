import sqlite3


def create_tables():
    # Create a database and connect
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurantTB (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        street_address TEXT,
        city TEXT,
        state TEXT,
        zipcode TEXT,
        curbside_pickup TEXT,
        delivery TEXT);
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cuisineTB (
        id INTEGER PRIMARY KEY,
        cuisine TEXT,
        restaurant TEXT,
        FOREIGN KEY(restaurant) REFERENCES restaurantTB(name)
        ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratingTB (
        id INTEGER PRIMARY KEY,
        restaurant TEXT,
        rating INTEGER,
        FOREIGN KEY(restaurant) REFERENCES restaurantTB(name)
        ON DELETE CASCADE
        );
    """)
    connection.commit()
    connection.close()


def insert_values():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO restaurantTB (name, street_address, city, state, zipcode, curbside_pickup, delivery) 
        VALUES ('Robin', '620 Gough St', 'San Francisco', 'CA', '94102', 'yes', 'yes'),
        ('The Shota', '115 Sansome St', 'San Francisco', 'CA', '94104', 'yes', 'no'),
        ('Aki', '1137 11th Ave', 'Honolulu', 'HI', '96814', 'no', 'yes'),
        ('Changs', '1311 SW 107th Ave', 'Miami', 'FL', '33174', 'yes', 'no'),
        ('Hue Restaurant', '3005 Silver Creek Rd', 'San Jose', 'CA', '95121', 'no', 'yes'),
        ('Shabuya', '84 Ranch Dr', 'Milpitas', 'CA', '95035', 'yes', 'no'),
        ('Spartan Taco', '515 S 10th St', 'San Jose', 'CA', '95112', 'yes', 'yes'),
        ('Alachi Masala', '488 Amsterdam Ave', 'New York', 'NY', '10024', 'yes', 'no'),
        ('Glur Thai', '144 W 19th St', 'New York', 'NY', '10011', 'no', 'yes'),
        ('BCD Tofu House', '5w 32nd St', 'New York', 'NY', '10001', 'yes', 'yes');
    """)

    # Insert values to cuisine table
    cursor.execute("""
        INSERT INTO cuisineTB (cuisine, restaurant) 
        VALUES ('Sushi', 'Robin'),
        ('Omasake', 'Robin'),
        ('Japanese', 'The Shota'),
        ('Combodian', 'Aki'),
        ('Malaysian', 'Aki'),
        ('Chinese', 'Changs'),
        ('Vietnamese', 'Changs'),
        ('Vietnamese', 'Hue Restaurant'),
        ('Hotpot', 'Shabuya'),
        ('Mexican', 'Spartan Taco'),
        ('Indian', 'Alachi Masala'),
        ('Thai', 'Glur Thai'),
        ('Combodian', 'Glur Thai'),
        ('Korean', 'BCD Tofu House')
        ;
    """)

    # Insert values to rating table
    cursor.execute("""
        INSERT INTO ratingTB (restaurant, rating) 
        VALUES ('Robin', 5),
        ('Robin', 4),
        ('The Shota', 3),
        ('The Shota', 5),
        ('Alachi Masala', 3),
        ('Aki', 4),
        ('Changs', 4),
        ('Hue Restaurant', 5),
        ('Shabuya', 4),
        ('Spartan Taco', 5),
        ('Glur Thai', 5),
        ('Glur Thai', 3),
        ('BCD Tofu House', 4)
        ;
    """)

    connection.commit()
    connection.close()
