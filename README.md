# Unified Fest Backend

Unified Fest Backend (UFB) provides a robust backend foundation for creating websites dedicated to college festivals. Instead of reinventing the wheel for every fest, our backend simplifies the process, enabling a quick start for web developers. Built on the Django framework, UFB offers a comprehensive collegiate festival template equipped with a plethora of features.

### Key Features
- Account Creation & Management: Register, log in, and manage user profiles with ease.
- Google Signup Integration: Seamlessly integrate Google signup for easier access.
- Event Registration: Register for events as individuals or teams, ensuring maximum flexibility.
- Sponsor Management: Efficiently manage and display festival sponsors.
- Team Management: Detailed section for team members, their roles, and more.
- Event Management: Create, edit, and display events hassle-free.
- PostgreSQL Integration: Robust database integration using PostgreSQL for data integrity and scalability.
- Clean and Modular Code: Ensuring UFB remains a versatile and easily customizable template for various needs.

## Setup and Installation
Follow these steps to set up the Unified Fest Backend on your local machine:
### 1. Install pipenv:
If you don't have `pipenv` installed, install it using `pip`:
```
pip install pipenv
```

### 2. Enter the pipenv shell:
Navigate to the root directory of the project and activate the `pipenv` shell:
```
pipenv shell
```

### 3. Install dependencies:
Install the required project dependencies:
```
pipenv install
```

### 4. Apply migrations:
Before running the server, ensure you've set up the database schema:
```
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the server:
Finally, start the Django development server:
```
python manage.py runserver
```

You should now see the server running on `http://127.0.0.1:8000/`. Open it in a web browser to start using the Unified Fest Backend.

### Build With
- Django

### Contributions
|Name|Year|Role|
|--|--|--|
|[Saahil Bhavsar](https://github.com/XanderWatson)|Final|Mentor|
|[Yuvraj Rathva](https://github.com/yuvrajrathva)|Pre-Final|Developer|
|[Prachiti Chandratreya](https://github.com/johngalt1618)|Sophomore|Developer|
