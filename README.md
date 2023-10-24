# DBMS-Project
The Registered Vehicle Management System is designed to facilitate the registration, tracking, and management of vehicles and their associated information.

**The roles defined in the system are:**
**Administrator:** Responsible for system configuration, user management, and
overall system control.
**Vehicle Owners:** Individuals who own and register vehicles. They can update their
vehicle information, renew registrations, and view violation and insurance records.

**Functional Requirements:**
**Vehicle Registration**
Vehicle owners can update their personal information, such as phone numbers
and addresses. Furthermore, they can also access a wealth of information about
their vehicles including license details, maintenance records, insurance policies,
inspection reports, and accident records.

**Vehicle Maintenance Records:**
Owners will be able to record and update maintenance records for their vehicles,
including service dates, service type, and cost just by entering the vehicle ID. The
system will provide maintenance history for each vehicle.

**Driver's License Management:**
Vehicle owners will be able to associate driver's license information with their
profiles, including license number and expiration date. The system will also send
renewal reminders.

**Vehicle Registration Renewal:**
Vehicle owners will receive reminders for registration renewal.
Registered Vehicle Management System

**Violation Tracking:**
Administrators will be able to record traffic violations, including date, time,
location, and violation type. Vehicle owners will be notified of violations and the
amount of fine that must be deposited within the due date.

**Accident Reporting:**
Vehicle owners will be able to report accidents, including date, location, license
number. Insurance information can be accessed with the help of vehicle ID
mentioned by the user.

**Vehicle Inspection Records:**
Owners will be able to view the inspection details, including inspection date and
results.

**Insurance Management:**
Vehicle owners will be able to associate insurance policies with their vehicles,
including policy number, coverage details, and expiration date. The system will
also send insurance renewal reminders.

**Reporting and Analytics:**
Administrators can generate reports which includes registration statistics,
violation trends, and accident summaries.

**Dependencies:**

python -m pip install --upgrade pip 

pip install flask

pip install mysql-connector-python --index-url=https://pypi.org/simple --trusted-host pypi.python.org

pip download mysql-connector-python
