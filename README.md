# 🚗 RideOnRentt - E-Car Rental System

A modern, full-stack web application designed to simplify the car rental process for customers and streamline vehicle and booking management for admins and car owners.

---

## 📖 Overview

This project was developed as part of the **Software Systems Design (CISE 5030)** course during Spring 2025 under the guidance of **Dr. Kamrul Hasan**. It enables users to register, browse available vehicles, book rentals, and make secure online payments. Car owners can list vehicles, and admins can manage listings and bookings through a dashboard.

---

## 🎯 Objectives

- Provide a user-friendly platform for car rental
- Enable real-time car availability and booking
- Automate the booking and payment process
- Improve administrative control and analytics

---

## 🔧 Features

- User Registration & Profile Management
- Car Inventory & Listing System
- Booking with Secure Online Payment
- Admin Dashboard for Approvals and Analytics
- Real-Time Notifications (Email/SMS)
- Role-based Access (User, Owner, Admin)

---

## 🧩 Technology Stack

| Layer               | Technology                         | Description                                   |
|--------------------|------------------------------------|-----------------------------------------------|
| Frontend           | HTML5, CSS, JavaScript, Bootstrap  | Responsive UI/UX                              |
| Backend            | Python, Django                     | Business logic and server-side operations     |
| Database           | MySQL/PostgreSQL                   | Persistent storage of bookings and users      |
| APIs/Integration   | REST APIs, OAuth                   | Social login, payments                        |
| Deployment         | AWS, Azure                         | Scalable and secure deployment                |

---

## 📊 Architecture

The system is structured using a layered architecture:

1. **Presentation Layer**: UI using Bootstrap, handles user interactions
2. **Application Layer**: Django views, forms, and business logic
3. **Data Access Layer**: ORM and raw SQL for secure data access
4. **Integration Layer**: RESTful APIs for payment and authentication
5. **Infrastructure Layer**: Cloud deployment (AWS/Azure)

---

## 🔁 System Flow

1. **User** registers/login → browses cars → selects car → books and pays
2. **Owner** submits car → awaits admin approval → gets listed
3. **Admin** manages inventory and bookings through dashboard

---

## 📈 Proposed Enhancements

- Mobile responsiveness and UX improvements
- Google Maps API for pick-up point navigation
- Multi-payment options (wallets, crypto)
- Analytics dashboard for admin insights
- Real-time notifications and 2FA security
- Customer feedback and review system

---

## 🗂️ Screenshots

📷 Screenshots included in the PDF (Pages 17–24)

---

## 📦 Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/yourusername/rideonrentt.git
cd rideonrentt
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirement.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create admin login
python manage.py runserver
