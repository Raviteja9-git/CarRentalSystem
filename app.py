# Flask Application

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime, timedelta


# Function to create tables if not present
def create_tables(cursor):
    # Dictionary of table names and their corresponding create table queries
    tables = {
        "Vehicles": """
            CREATE TABLE IF NOT EXISTS Vehicles (
                vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
                make VARCHAR(50),
                model VARCHAR(50),
                year INT,
                price_per_day DECIMAL(10,2),
                availability TINYINT(1)
            )
        """,
        "Customers": """
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100),
                phone_number VARCHAR(20)
            )
        """,
        "Bookings": """
            CREATE TABLE IF NOT EXISTS Bookings (
                booking_id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT,
                customer_id INT,
                pickup_date DATE,
                return_date DATE,
                total_cost DECIMAL(10,2),
                FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            )
        """,
        "Administrators": """
            CREATE TABLE IF NOT EXISTS Administrators (
                admin_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                password VARCHAR(50)
            )
        """,
    }

    # Execute create table queries for each table
    for table_name, create_query in tables.items():
        cursor.execute(create_query)


# Function to insert initial data into the Vehicles table
def insert_initial_data(cursor):
    # List of tuples containing car details (make, model, year, price_per_day, availability)
    cars_data = [
        ("Toyota", "Camry", 2022, 50.00, True),
        ("Honda", "Civic", 2021, 45.00, True),
        ("Ford", "Mustang", 2020, 70.00, True),
        ("Chevrolet", "Malibu", 2019, 55.00, True),
        ("Tesla", "Model 3", 2023, 100.00, True),
        ("BMW", "X5", 2021, 90.00, True),
        ("Mercedes-Benz", "E-Class", 2022, 80.00, True),
        ("Audi", "A4", 2020, 75.00, True),
        ("Lexus", "RX", 2023, 95.00, True),
        ("Jeep", "Wrangler", 2021, 65.00, True),
        ("Hyundai", "Elantra", 2022, 40.00, True),
        ("Kia", "Sorento", 2021, 60.00, True),
        ("Subaru", "Outback", 2020, 55.00, True),
        ("Mazda", "CX-5", 2023, 65.00, True),
        ("Nissan", "Altima", 2021, 50.00, True),
        ("Volvo", "XC60", 2022, 85.00, True),
        ("Infiniti", "Q50", 2020, 70.00, True),
        ("Porsche", "911", 2023, 150.00, True),
        ("Jaguar", "F-Pace", 2021, 110.00, True),
        ("Land Rover", "Discovery", 2022, 120.00, True),
    ]

    # Insert initial data into the Vehicles table
    for car in cars_data:
        insert_query = """
            INSERT INTO Vehicles (make, model, year, price_per_day, availability)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, car)


# Initialize Flask application
app = Flask(__name__)

# Initialize MySQL connection with configuration
mysql_conn = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL host
    user="root",  # Replace with your MySQL username
    password="yogesh14",  # Replace with your MySQL password
    database="car_rental_db",  # Replace with your MySQL database name
)

# Create cursor
cursor = mysql_conn.cursor()

# Check and create tables if not present
create_tables(cursor)

# Insert initial data into Vehicles table if it's empty
cursor.execute("SELECT COUNT(*) FROM Vehicles")
count = cursor.fetchone()[0]
if count == 0:
    insert_initial_data(cursor)
    mysql_conn.commit()


def calculate_total_cost(pickup_date, return_date, price_per_day):
    # Convert string dates to datetime objects
    pickup_date_obj = datetime.strptime(pickup_date, "%Y-%m-%d")
    return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")

    # Calculate number of rental days
    rental_days = (return_date_obj - pickup_date_obj).days

    # Calculate total cost
    total_cost = rental_days * price_per_day
    return total_cost


@app.route("/", methods=["GET", "POST"])
def home():
    try:
        # Fetch car data from the Vehicles table
        cursor.execute("SELECT * FROM Vehicles")
        cars = cursor.fetchall()  # Fetch all cars
    except mysql.connector.Error as error:
        cars = []
        error_message = "Error fetching car data."

    if request.method == "POST":
        return render_template("index.html", cars=cars)
    else:
        return render_template("index.html", cars=cars)


@app.route("/view-joined-table", methods=["POST"])
def view_joined_table():
    try:
        # Perform the join between Vehicles and Bookings tables
        cursor.execute(
            """
            SELECT Vehicles.*, Bookings.pickup_date, Bookings.return_date, Bookings.total_cost
            FROM Vehicles
            INNER JOIN Bookings ON Vehicles.vehicle_id = Bookings.vehicle_id
        """
        )
        table_columns = [i[0] for i in cursor.description]
        table_data = cursor.fetchall()

        return render_template(
            "view_tables.html", table_columns=table_columns, table_data=table_data
        )
    except mysql.connector.Error as error:
        error_message = "Error fetching joined data."
        return render_template("view_tables.html", error_message=error_message)


@app.route("/view-tables", methods=["GET", "POST"])
def view_tables():
    if request.method == "POST":
        table_name = request.form.get("table")
        try:
            if table_name == "Vehicles":
                cursor.execute("SELECT * FROM Vehicles")
            elif table_name == "Customers":
                cursor.execute("SELECT * FROM Customers")
            elif table_name == "Bookings":
                cursor.execute("SELECT * FROM Bookings")
            elif table_name == "Administrators":
                cursor.execute("SELECT * FROM Administrators")
            else:
                error_message = "Invalid table selected."
                return render_template("view_tables.html", error_message=error_message)

            table_columns = [i[0] for i in cursor.description]
            table_data = cursor.fetchall()

            return render_template(
                "view_tables.html", table_columns=table_columns, table_data=table_data
            )
        except mysql.connector.Error as error:
            error_message = "Error fetching data from the table."
            return render_template("view_tables.html", error_message=error_message)
    else:
        return render_template("view_tables.html")


# Rent car route
@app.route("/rent", methods=["POST"])
def rent_car():
    try:
        vehicle_id = request.form.get("vehicleId")
        pickup_date = request.form.get("pickupDate")
        return_date = request.form.get("returnDate")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        phone_number = request.form.get("phoneNumber")

        # Connect to MySQL
        mysql_conn = mysql.connector.connect(
            host="localhost", user="root", password="yogesh14", database="car_rental_db"
        )
        cursor = mysql_conn.cursor()

        # Insert the user into the Customers table
        insert_customer_query = """
        INSERT INTO Customers (first_name, last_name, email, phone_number)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            insert_customer_query, (first_name, last_name, email, phone_number)
        )
        mysql_conn.commit()
        customer_id = cursor.lastrowid

        # Change the availability of the car to False
        update_availability_query = """
        UPDATE Vehicles
        SET availability = False
        WHERE vehicle_id = %s
        """
        cursor.execute(update_availability_query, (vehicle_id,))
        mysql_conn.commit()

        # Calculate total cost
        cursor.execute(
            "SELECT price_per_day FROM Vehicles WHERE vehicle_id = %s", (vehicle_id,)
        )
        price_per_day = cursor.fetchone()[0]
        total_cost = calculate_total_cost(pickup_date, return_date, price_per_day)

        # Add rental booking to the Bookings table
        insert_booking_query = """
        INSERT INTO Bookings (vehicle_id, customer_id, pickup_date, return_date, total_cost)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_booking_query,
            (vehicle_id, customer_id, pickup_date, return_date, total_cost),
        )
        mysql_conn.commit()

        return redirect(url_for("rent_success"))

    except mysql.connector.Error as error:
        return render_template("error.html", message="Error renting car.")

    finally:
        # Close cursor and connection
        cursor.close()
        mysql_conn.close()


# Rent success route
@app.route("/rent-success")
def rent_success():
    return render_template("rent_success.html")


if __name__ == "__main__":
    app.run(debug=True)
