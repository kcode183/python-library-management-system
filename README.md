# Python Library Management System

A command line library management system built with Python to manage books, users, borrowing, returns, and library activity.

I developed this project to practice building a larger Python application with multiple interconnected features, persistent data storage, user roles, and reporting.


### User Features
- User login
- View all books and their availability
- Search by title, partial title, author, or category
- Sort books by title, author, category, or availability
- View book categories
- Borrow available books
- Return borrowed books
- View currently borrowed books

### Administrator Features
- Separate administrator menu
- Add new books and additional copies
- Remove books when no copies are currently borrowed
- View borrowing activity
- View library statistics
- Search, sort, and browse the library collection

### Data & Reporting
- JSON based persistent data storage
- Book availability and copy tracking
- Borrowing history with timestamps
- Borrowing frequency tracking
- Most borrowed-book statistics
- Category statistics
- Automatic book ID generation

## Technologies Used

- Python
- JSON
- File handling
- Command-line interface

## Data Storage

The application automatically creates and maintains:

- `books.json` — book inventory and availability
- `users.json` — user accounts and borrowed books
- `activity.json` — borrowing and return activity

## Running the Project

1. Install Python 3.
2. Download or clone this repository.
3. Run: "python python-library-management-system.py"
