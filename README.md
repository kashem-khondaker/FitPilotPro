# Gym Management System

## Overview

The Gym Management System is a comprehensive web application designed to manage gym operations efficiently. It provides role-based access control for Members, Staff, and Admins, ensuring secure and streamlined management of memberships, fitness classes, attendance, payments, feedback, and reports.

## Features

### 1. User Authentication

- Three roles: Member, Staff, and Admin.
- User registration, login, and logout for all roles.
- Email verification for account activation.
- Only verified users can log in.

### 2. Membership and Subscription Management

- Staff can create, update, and delete membership plans (e.g., Weekly, Monthly, Yearly).
- Members can view and update their own subscription plans.
- Admin can manage all membership plans and subscriptions.

### 3. Fitness Classes and Scheduling

- Staff can add, update, and delete fitness classes (e.g., yoga, Zumba, cardio).
- Members can view class schedules, instructors, and class details.
- Members can book classes online and view their booking history.
- Admin can manage all classes and bookings.

### 4. Attendance Tracking

- Staff can mark attendance for Members in fitness classes.
- Members can view their attendance history.
- Admin can view attendance reports for all classes.

### 5. Payment Management

- Members can make payments for their subscription plans.
- Staff can view payment history for Members.
- Admin can manage all payments and generate payment reports.

### 6. Feedback and Reviews

- Members can leave feedback and reviews for fitness classes.
- Staff can view feedback and reviews for their classes.
- Admin can view all feedback and reviews.

### 7. Reports and Analytics

- Admin can generate reports and analytics for:
  - Memberships
  - Attendance
  - Feedback

### 8. Deployment

- The application is deployed on a secure and scalable hosting platform.

## Installation

### Prerequisites

- Python 3.13 or higher
- Virtual environment (recommended)
- Django and required dependencies

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd Gym Management System/FitPilotPro
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/Scripts/activate  # On Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Use the Admin panel at `http://127.0.0.1:8000/admin/` for administrative tasks.

## Testing

- Run tests using:
  ```bash
  python manage.py test
  ```

## Contributing

- Fork the repository and create a pull request for any enhancements or bug fixes.

## License

- This project is licensed under the MIT License.
