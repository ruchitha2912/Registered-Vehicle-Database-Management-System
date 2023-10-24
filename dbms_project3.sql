DROP SCHEMA IF EXISTS registerd_vehicles;
CREATE SCHEMA IF NOT EXISTS registered_vehicles;
USE registered_vehicles;

CREATE TABLE IF NOT EXISTS Owners(
Owner_id VARCHAR(30) PRIMARY KEY,
Owner_name VARCHAR(255) NOT NULL,
Owner_phone VARCHAR(30) NOT NULL,
License_number VARCHAR(30) NOT NULL,
Gender CHAR(1) NOT NULL,
Address TEXT NOT NULL,
Dob DATE NOT NULL
);

INSERT INTO Owners (Owner_id, Owner_name, License_number, Owner_phone, Gender, Address, Dob)
VALUES
    ('1', 'John Smith', '555-123-4567', 'LIC12345', 'M', '123 Main St, Anytown, USA', '1990-05-15'),
    ('2', 'Jane Doe', '555-987-6543', 'LIC54321', 'F', '456 Elm St, Othertown, USA', '1985-09-22'),
    ('3', 'Michael Johnson', '555-555-5555', 'LIC78901', 'M', '789 Oak St, Differenttown, USA', '1978-03-10'),
    ('4', 'Sarah White', '555-333-2222', 'LIC45678', 'F', '321 Maple St, Anothertown, USA', '1995-12-07'),
    ('5', 'Robert Brown', '555-777-8888', 'LIC23456', 'M', '555 Pine St, Nearbytown, USA', '1980-07-18'),
    ('6', 'Lisa Johnson', '555-222-3333', 'LIC98765', 'F', '987 Cedar St, Farawaytown, USA', '1987-02-25'),
    ('7', 'Daniel Lee', '555-444-9999', 'LIC65432', 'M', '654 Birch St, Distanttown, USA', '1992-11-30'),
    ('8', 'Emily Clark', '555-666-1111', 'LIC87654', 'F', '222 Spruce St, Remoteville, USA', '1975-06-03');

CREATE TABLE IF NOT EXISTS License(
License_number VARCHAR(30) PRIMARY KEY,
Owner_id VARCHAR(30),
Issue_date DATE NOT NULL,
Expiry_date DATE NOT NULL,
Vehicle_type TEXT,
FOREIGN KEY (Owner_id) REFERENCES Owners(Owner_id)
);

INSERT INTO License (License_number, Owner_id, Issue_date, Expiry_date, Vehicle_type)
VALUES
    ('LIC12345', '1', '2022-03-15', '2023-03-14', 'Car'),
    ('LIC54321', '2', '2022-05-20', '2023-05-19', 'Motorcycle'),
    ('LIC78901', '3', '2022-01-10', '2023-01-09', 'Car'),
    ('LIC45678', '4', '2022-08-05', '2023-08-04', 'Car'),
    ('LIC23456', '5', '2022-06-30', '2023-06-29', 'Motorcycle'),
    ('LIC98765', '6', '2022-04-22', '2023-04-21', 'Car'),
    ('LIC65432', '7', '2022-02-14', '2023-02-13', 'Motorcycle'),
    ('LIC87654', '8', '2022-07-09', '2023-07-08', 'Car'),
    ('LIC34567', '1', '2022-10-12', '2023-10-11', 'Motorcycle'),
    ('LIC56789', '2', '2022-11-28', '2023-11-27', 'Car');


CREATE TABLE IF NOT EXISTS Vehicle(
Vehicle_id VARCHAR(50) PRIMARY KEY,
RegNumber VARCHAR(50) NOT NULL,
Model VARCHAR(50) NOT NULL,
Owner_id VARCHAR(30),
Reg_year DATE NOT NULL,
NumberPlate VARCHAR(30) NOT NULL,
VehicleType VARCHAR(30) NOT NULL,
Vehicle_description TEXT,
FOREIGN KEY (Owner_id) REFERENCES Owners(Owner_id)
);

INSERT INTO Vehicle (Vehicle_id, RegNumber, Model, Owner_id, Reg_year, NumberPlate, VehicleType, Vehicle_description)
VALUES
    ('CAR001', 'AB123CD', 'Toyota Corolla', '1', '2019-05-10', 'CAR-ABC-123', 'Car', 'Sedan, Silver color'),
    ('CAR002', 'XY456Z', 'Honda Civic', '2', '2020-03-15', 'CAR-XYZ-456', 'Car', 'Hatchback, Red color'),
    ('BIKE001', 'DEF789', 'Yamaha FZ', '3', '2018-07-20', 'BIKE-DEF-789', 'Motorcycle', 'Sports bike, Blue color'),
    ('CAR003', 'GH56	7JK', 'Ford Mustang', '4', '2021-01-05', 'CAR-GHJ-567', 'Car', 'Sports car, Yellow color'),
    ('BIKE002', 'LMN456', 'Kawasaki Ninja', '5', '2019-11-30', 'BIKE-LMN-456', 'Motorcycle', 'Superbike, Green color'),
    ('CAR004', 'PQR123', 'Chevrolet Malibu', '6', '2017-12-22', 'CAR-PQR-123', 'Car', 'Sedan, Black color'),
    ('BIKE003', 'STU987', 'Suzuki GSX-R', '7', '2020-08-18', 'BIKE-STU-987', 'Motorcycle', 'Sports bike, Red and Black'),
    ('CAR005', 'VWX789', 'BMW X5', '8', '2018-04-05', 'CAR-VWX-789', 'Car', 'SUV, White color'),
    ('CAR006', 'YZA456', 'Audi A4', '1', '2021-10-15', 'CAR-YZA-456', 'Car', 'Luxury sedan, Silver color'),
    ('BIKE004', 'BCD123', 'Ducati Panigale', '2', '2019-09-28', 'BIKE-BCD-123', 'Motorcycle', 'Superbike, Red color');


CREATE TABLE IF NOT EXISTS Inspection(
Inspection_id VARCHAR(50) PRIMARY KEY,
Inspector_Name VARCHAR(30),
Result BOOLEAN NOT NULL,
Inspection_date DATE NOT NULL,
Vehicle_id VARCHAR(50),
FOREIGN KEY (Vehicle_id) REFERENCES Vehicle(Vehicle_id)
);

INSERT INTO Inspection (Inspection_id, Inspector_Name, Result, Inspection_date, Vehicle_id)
VALUES
    ('INSP001', 'John Inspector', true, '2023-01-15', 'CAR001'),
    ('INSP002', 'Lisa Inspector', true, '2023-02-20', 'CAR002'),
    ('INSP003', 'Michael Inspector', false, '2023-03-10', 'BIKE001'),
    ('INSP004', 'Sarah Inspector', true, '2023-04-05', 'CAR003'),
    ('INSP005', 'Daniel Inspector', true, '2023-05-30', 'BIKE002'),
    ('INSP006', 'Emily Inspector', true, '2023-06-22', 'CAR004'),
    ('INSP007', 'Robert Inspector', true, '2023-07-18', 'BIKE003'),
    ('INSP008', 'Jane Inspector', false, '2023-08-10', 'CAR005'),
    ('INSP009', 'John Inspector', true, '2023-09-15', 'CAR006'),
    ('INSP010', 'Lisa Inspector', true, '2023-10-28', 'BIKE004');


CREATE TABLE IF NOT EXISTS Accident(
Accident_id VARCHAR(30) PRIMARY KEY,
License_number VARCHAR(30),
Vehicle_id VARCHAR(50),
Location VARCHAR(30) NOT NULL,
Accident_date DATE NOT NULL,
Accident_description TEXT,
FOREIGN KEY (License_number) REFERENCES License(License_number),
FOREIGN KEY (Vehicle_id) REFERENCES Vehicle(Vehicle_id)
);

INSERT INTO Accident (Accident_id, License_number, Vehicle_id, Location, Accident_date, Accident_description)
VALUES
    ('ACC001', 'LIC12345', 'CAR001', 'Main Street', '2023-03-25', 'Fender bender, minor damage'),
    ('ACC002', 'LIC54321', 'BIKE001', 'Park Avenue', '2023-04-10', 'Rear-end collision, no injuries'),
    ('ACC003', 'LIC78901', 'CAR003', 'Highway 101', '2023-05-15', 'Multiple car pileup, injuries reported'),
    ('ACC004', 'LIC45678', 'CAR004', 'Elm Street', '2023-06-02', 'Side collision, moderate damage');


CREATE TABLE IF NOT EXISTS Violation(
Violation_id VARCHAR(30) PRIMARY KEY,
Vehicle_id VARCHAR(50),
Fine_amount INT NOT NULL,
violation_date DATE NOT NULL,
violation_type VARCHAR(30) NOT NULL,
FOREIGN KEY (Vehicle_id) REFERENCES Vehicle(Vehicle_id)
);

INSERT INTO Violation (Violation_id, Vehicle_id, Fine_amount, violation_date, violation_type)
VALUES
    ('VIOL001', 'CAR001', 100, '2023-04-05', 'Speeding'),
    ('VIOL002', 'CAR002', 50, '2023-04-12', 'Parking Violation'),
    ('VIOL003', 'BIKE001', 75, '2023-05-20', 'Running Red Light');


CREATE TABLE IF NOT EXISTS Maintenance(
Service_id VARCHAR(20) PRIMARY KEY,
Vehicle_id VARCHAR(50),
Service_cost INT NOT NULL,
Service_date DATE NOT NULL,
Next_Service_date DATE NOT NULL,
Details TEXT,
FOREIGN KEY (Vehicle_id) REFERENCES Vehicle(Vehicle_id)
);

INSERT INTO Maintenance (Service_id, Vehicle_id, Service_cost, Service_date, Next_Service_date, Details)
VALUES
    ('SERV001', 'CAR001', 150, '2023-03-05', '2023-09-05', 'Oil change and tire rotation'),
    ('SERV002', 'CAR002', 200, '2023-04-10', '2023-10-10', 'Brake pad replacement and engine check'),
    ('SERV003', 'BIKE001', 80, '2023-05-15', '2023-11-15', 'Chain lubrication and general checkup'),
    ('SERV004', 'CAR003', 120, '2023-06-20', '2023-12-20', 'Transmission fluid change and alignment check'),
    ('SERV005', 'BIKE002', 60, '2023-07-25', '2024-01-25', 'Tire replacement and spark plug change'),
    ('SERV006', 'CAR004', 180, '2023-08-30', '2024-02-28', 'Wheel alignment and exhaust system inspection'),
    ('SERV007', 'BIKE003', 70, '2023-09-05', '2024-03-05', 'Carburetor cleaning and chain tension adjustment'),
    ('SERV008', 'CAR005', 140, '2023-10-10', '2024-04-10', 'Air filter replacement and brake fluid flush'),
    ('SERV009', 'CAR006', 160, '2023-11-15', '2024-05-15', 'Coolant flush and transmission check'),
    ('SERV010', 'BIKE004', 90, '2023-12-20', '2024-06-20', 'Oil filter replacement and battery check');


CREATE TABLE IF NOT EXISTS Registration(
Register_id VARCHAR(30) PRIMARY KEY,
Vehicle_id VARCHAR(50),
Owner_id VARCHAR(30),
Reg_date DATE NOT NULL,
Renewal_date DATE NOT NULL,
FOREIGN KEY (Vehicle_id) REFERENCES Vehicle(Vehicle_id),
FOREIGN KEY (Owner_id) REFERENCES Owners(Owner_id)
);

INSERT INTO Registration (Register_id, Vehicle_id, Owner_id, Reg_date, Renewal_date)
VALUES
    ('REG001', 'CAR001', '1', '2023-02-15', '2024-02-14'),
    ('REG002', 'CAR002', '2', '2023-03-20', '2024-03-19'),
    ('REG003', 'BIKE001', '3', '2023-04-10', '2024-04-09'),
    ('REG004', 'CAR003', '4', '2023-05-05', '2024-05-04'),
    ('REG005', 'BIKE002', '5', '2023-06-30', '2024-06-29'),
    ('REG006', 'CAR004', '6', '2023-07-15', '2024-07-14'),
    ('REG007', 'BIKE003', '7', '2023-08-25', '2024-08-24'),
    ('REG008', 'CAR005', '8', '2023-09-10', '2024-09-09'),
    ('REG009', 'CAR006', '1', '2023-10-20', '2024-10-19'),
    ('REG010', 'BIKE004', '2', '2023-11-05', '2024-11-04');


CREATE TABLE IF NOT EXISTS Insurance(
Policy_number VARCHAR(20) PRIMARY KEY,
Vehicle_id VARCHAR(50),
Owner_id VARCHAR(30),
Coverage_details TEXT,
Coverage_amt INT NOT NULL,
Insurance_cmpy VARCHAR(30) NOT NULL,
Insurance_expiry DATE NOT NULL,
FOREIGN KEY (Vehicle_id) REFERENCES Vehicle(Vehicle_id),
FOREIGN KEY (Owner_id) REFERENCES Owners(Owner_id)
);

INSERT INTO Insurance (Policy_number, Vehicle_id, Owner_id, Coverage_details, Coverage_amt, Insurance_cmpy, Insurance_expiry)
VALUES
    ('POL001', 'CAR001', '1', 'Comprehensive coverage', 1000, 'ABC Insurance', '2024-03-01'),
    ('POL002', 'CAR002', '2', 'Liability coverage', 500, 'XYZ Insurance', '2024-04-15'),
    ('POL003', 'BIKE001', '3', 'Collision coverage', 800, 'DEF Insurance', '2024-05-10'),
    ('POL004', 'CAR003', '4', 'Comprehensive coverage', 1200, 'GHI Insurance', '2024-06-05'),
    ('POL005', 'BIKE002', '5', 'Liability coverage', 600, 'JKL Insurance', '2024-07-20'),
    ('POL006', 'CAR004', '6', 'Collision coverage', 900, 'MNO Insurance', '2024-08-15'),
    ('POL007', 'BIKE003', '7', 'Comprehensive coverage', 1100, 'PQR Insurance', '2024-09-30'),
    ('POL008', 'CAR005', '8', 'Liability coverage', 550, 'STU Insurance', '2024-10-25'),
    ('POL009', 'CAR006', '1', 'Collision coverage', 950, 'VWX Insurance', '2024-11-20'),
    ('POL010', 'BIKE004', '2', 'Comprehensive coverage', 1300, 'YZA Insurance', '2024-12-05');





