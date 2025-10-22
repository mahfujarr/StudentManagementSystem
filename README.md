# Student Management System

A web-based application for managing student records, fees collection, and administrative tasks for educational institutions.

## Features

- **Student Management**
  - Add, edit, view, and delete student profiles
  - Upload and manage student images
  - Auto-generate student IDs based on session
  - Store parent and address information

- **Fees Collection**
  - Add and track student fee payments
  - View payment summaries and outstanding balances
  - Download fee reports

- **User Authentication**
  - Admin login and registration
  - Password reset and recovery

- **Dashboard**
  - Overview of total students, revenue, awards, and departments
  - Recent student activities

- **Responsive UI**
  - Modern Bootstrap-based interface
  - Mobile-friendly design

## Project Structure

```
ZCA/
├── manage.py
├── db.sqlite3
├── students/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py
│   └── ...
├── ZCA/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── student-list.html
│   ├── student-add.html
│   ├── student-edit.html
│   ├── student-details.html
│   ├── fees-collections.html
│   ├── view-fees.html
│   ├── login.html
│   ├── register.html
│   ├── forgot-password.html
│   └── reset-password.html
├── static/
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   └── plugins/
│   └── ...
├── media/
│   └── student_img/
└── README.md
```

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd ZCA
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Apply migrations**
   ```sh
   python manage.py migrate
   ```

4. **Create a superuser**
   ```sh
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```sh
   python manage.py runserver
   ```

6. **Access the application**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage

- Log in as an admin to access the dashboard.
- Use the sidebar to navigate between students, fees collection, and other management features.
- Add or edit student information, manage fee payments, and view reports.

## Technologies Used

- Django (Python)
- Bootstrap 4
- jQuery
- SQLite (default, can be changed)
- FontAwesome


**Note:** Update `settings.py` for production use (e.g., static/media paths, database, secret key).