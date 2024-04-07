-- Retrieve all vehicles
SELECT * FROM Vehicles;

-- Retrieve all customers
SELECT * FROM Customers;

-- Retrieve all bookings
SELECT * FROM Bookings;

-- Retrieve all administrators
SELECT * FROM Administrators;

-- Insert a new vehicle
INSERT INTO Vehicles (make, model, year, price_per_day, availability)
VALUES ('Toyota', 'Corolla', 2023, 55.00, 1);

-- Update a vehicle's price
UPDATE Vehicles SET price_per_day = 60.00 WHERE model = 'Corolla';

-- Delete a vehicle
DELETE FROM Vehicles WHERE model = 'Corolla';

-- Insert a new customer
INSERT INTO Customers (first_name, last_name, email, phone_number)
VALUES ('John', 'Doe', 'john.doe@example.com', '+1234567890');

-- Update a customer's email
UPDATE Customers SET email = 'john_new@example.com' WHERE last_name = 'Doe';

-- Delete a customer
DELETE FROM Customers WHERE last_name = 'Doe';

-- Insert a new booking
INSERT INTO Bookings (vehicle_id, customer_id, pickup_date, return_date, total_cost)
VALUES (1, 1, '2024-04-01', '2024-04-05', 250.00);

-- Update a booking's return date
UPDATE Bookings SET return_date = '2024-04-06' WHERE booking_id = 1;

-- Delete a booking
DELETE FROM Bookings WHERE booking_id = 1;
