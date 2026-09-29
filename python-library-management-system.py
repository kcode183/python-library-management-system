import json
import os
from datetime import datetime


# --------------------------------------------------
# FILE NAMES
# --------------------------------------------------

BOOKS_FILE = "books.json"
USERS_FILE = "users.json"
ACTIVITY_FILE = "activity.json"


# --------------------------------------------------
# JSON FILE FUNCTIONS
# --------------------------------------------------

def load_json(filename, default_data):
    if not os.path.exists(filename):
        save_json(filename, default_data)
        return default_data

    try:
        with open(filename, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return default_data


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# --------------------------------------------------
# DEFAULT DATA
# --------------------------------------------------

default_books = [
    {
        "id": "B001",
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "category": "Fantasy",
        "total_copies": 3,
        "available_copies": 3,
        "times_borrowed": 0
    },
    {
        "id": "B002",
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "category": "Fantasy",
        "total_copies": 2,
        "available_copies": 2,
        "times_borrowed": 0
    },
    {
        "id": "B003",
        "title": "1984",
        "author": "George Orwell",
        "category": "Dystopian",
        "total_copies": 4,
        "available_copies": 4,
        "times_borrowed": 0
    }
]


default_users = [
    {
        "username": "admin",
        "password": "admin123",
        "role": "admin",
        "borrowed_books": []
    },
    {
        "username": "student",
        "password": "student123",
        "role": "user",
        "borrowed_books": []
    }
]


books = load_json(BOOKS_FILE, default_books)
users = load_json(USERS_FILE, default_users)
activity = load_json(ACTIVITY_FILE, [])


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def pause():
    input("\nPress Enter to continue...")


def generate_book_id():
    if len(books) == 0:
        return "B001"

    numbers = []

    for book in books:
        try:
            number = int(book["id"][1:])
            numbers.append(number)
        except ValueError:
            pass

    if not numbers:
        return "B001"

    next_number = max(numbers) + 1

    return f"B{next_number:03}"


def find_book_by_id(book_id):
    for book in books:
        if book["id"].lower() == book_id.lower():
            return book

    return None


def find_user(username):
    for user in users:
        if user["username"].lower() == username.lower():
            return user

    return None


def record_activity(username, book, action):
    activity_record = {
        "username": username,
        "book_id": book["id"],
        "title": book["title"],
        "action": action,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    activity.append(activity_record)
    save_json(ACTIVITY_FILE, activity)


# --------------------------------------------------
# DISPLAY BOOKS
# --------------------------------------------------

def display_books(book_list=None):

    if book_list is None:
        book_list = books

    if len(book_list) == 0:
        print("\nNo books found.")
        return

    print("\n" + "=" * 100)

    print(
        f"{'ID':<7}"
        f"{'Title':<35}"
        f"{'Author':<25}"
        f"{'Category':<15}"
        f"{'Available':<10}"
    )

    print("=" * 100)

    for book in book_list:

        availability = (
            f"{book['available_copies']}/"
            f"{book['total_copies']}"
        )

        print(
            f"{book['id']:<7}"
            f"{book['title'][:33]:<35}"
            f"{book['author'][:23]:<25}"
            f"{book['category'][:13]:<15}"
            f"{availability:<10}"
        )

    print("=" * 100)


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

def search_books():

    search_term = input(
        "\nEnter title, partial title, author, or category: "
    ).lower()

    results = []

    for book in books:

        if (
            search_term in book["title"].lower()
            or search_term in book["author"].lower()
            or search_term in book["category"].lower()
        ):
            results.append(book)

    if results:
        print("\nSearch Results:")
        display_books(results)

    else:
        print("\nNo matching books found.")


# --------------------------------------------------
# CATEGORY DISPLAY
# --------------------------------------------------

def display_categories():

    categories = sorted(
        set(book["category"] for book in books)
    )

    print("\nBOOK CATEGORIES")
    print("-" * 30)

    for category in categories:
        print(category)


# --------------------------------------------------
# SORT BOOKS
# --------------------------------------------------

def sort_books():

    print("\nSORT BOOKS")
    print("1. Title")
    print("2. Author")
    print("3. Category")
    print("4. Available copies")

    choice = input("\nChoose sorting method: ")

    if choice == "1":
        sorted_books = sorted(
            books,
            key=lambda book: book["title"].lower()
        )

    elif choice == "2":
        sorted_books = sorted(
            books,
            key=lambda book: book["author"].lower()
        )

    elif choice == "3":
        sorted_books = sorted(
            books,
            key=lambda book: book["category"].lower()
        )

    elif choice == "4":
        sorted_books = sorted(
            books,
            key=lambda book: book["available_copies"],
            reverse=True
        )

    else:
        print("Invalid option.")
        return

    display_books(sorted_books)


# --------------------------------------------------
# ADMIN - ADD BOOK
# --------------------------------------------------

def add_book():

    print("\nADD BOOK")
    print("-" * 30)

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    category = input("Category: ").strip()

    try:
        copies = int(input("Number of copies: "))

        if copies <= 0:
            print("Copies must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    # Check if the same book already exists

    for book in books:

        if (
            book["title"].lower() == title.lower()
            and book["author"].lower() == author.lower()
        ):

            book["total_copies"] += copies
            book["available_copies"] += copies

            save_json(BOOKS_FILE, books)

            print(
                f"\nAdded {copies} additional copies "
                f"of '{title}'."
            )

            return

    new_book = {
        "id": generate_book_id(),
        "title": title,
        "author": author,
        "category": category,
        "total_copies": copies,
        "available_copies": copies,
        "times_borrowed": 0
    }

    books.append(new_book)

    save_json(BOOKS_FILE, books)

    print(
        f"\nBook added successfully with ID "
        f"{new_book['id']}."
    )


# --------------------------------------------------
# ADMIN - REMOVE BOOK
# --------------------------------------------------

def remove_book():

    display_books()

    book_id = input(
        "\nEnter the ID of the book to remove: "
    )

    book = find_book_by_id(book_id)

    if book is None:
        print("Book not found.")
        return

    borrowed_copies = (
        book["total_copies"]
        - book["available_copies"]
    )

    if borrowed_copies > 0:

        print(
            "\nThis book cannot be removed because "
            "copies are currently borrowed."
        )

        return

    books.remove(book)

    save_json(BOOKS_FILE, books)

    print(
        f"\n'{book['title']}' has been removed."
    )


# --------------------------------------------------
# BORROW BOOK
# --------------------------------------------------

def borrow_book(user):

    display_books()

    book_id = input(
        "\nEnter the ID of the book you want to borrow: "
    )

    book = find_book_by_id(book_id)

    if book is None:
        print("Book not found.")
        return

    if book["available_copies"] <= 0:
        print("No copies are currently available.")
        return

    if book["id"] in user["borrowed_books"]:
        print("You have already borrowed this book.")
        return

    book["available_copies"] -= 1
    book["times_borrowed"] += 1

    user["borrowed_books"].append(
        book["id"]
    )

    save_json(BOOKS_FILE, books)
    save_json(USERS_FILE, users)

    record_activity(
        user["username"],
        book,
        "BORROWED"
    )

    print(
        f"\nYou borrowed '{book['title']}'."
    )


# --------------------------------------------------
# RETURN BOOK
# --------------------------------------------------

def return_book(user):

    if len(user["borrowed_books"]) == 0:
        print("\nYou have no borrowed books.")
        return

    borrowed = []

    for book_id in user["borrowed_books"]:

        book = find_book_by_id(book_id)

        if book:
            borrowed.append(book)

    print("\nYOUR BORROWED BOOKS")

    display_books(borrowed)

    book_id = input(
        "\nEnter the ID of the book to return: "
    )

    if book_id not in user["borrowed_books"]:
        print("You have not borrowed that book.")
        return

    book = find_book_by_id(book_id)

    if book is None:
        print("Book record could not be found.")
        return

    book["available_copies"] += 1

    user["borrowed_books"].remove(
        book_id
    )

    save_json(BOOKS_FILE, books)
    save_json(USERS_FILE, users)

    record_activity(
        user["username"],
        book,
        "RETURNED"
    )

    print(
        f"\nYou returned '{book['title']}'."
    )


# --------------------------------------------------
# USER BORROWED BOOKS
# --------------------------------------------------

def display_borrowed_books(user):

    if not user["borrowed_books"]:
        print("\nYou have no borrowed books.")
        return

    borrowed = []

    for book_id in user["borrowed_books"]:

        book = find_book_by_id(book_id)

        if book:
            borrowed.append(book)

    print("\nYOUR BORROWED BOOKS")

    display_books(borrowed)


# --------------------------------------------------
# ACTIVITY REPORT
# --------------------------------------------------

def show_activity():

    if len(activity) == 0:
        print("\nNo borrowing activity recorded.")
        return

    print("\nBORROWING ACTIVITY")
    print("=" * 100)

    print(
        f"{'User':<15}"
        f"{'Book':<35}"
        f"{'Action':<12}"
        f"{'Date':<20}"
    )

    print("=" * 100)

    for record in activity:

        print(
            f"{record['username']:<15}"
            f"{record['title'][:33]:<35}"
            f"{record['action']:<12}"
            f"{record['date']:<20}"
        )

    print("=" * 100)


# --------------------------------------------------
# STATISTICS
# --------------------------------------------------

def show_statistics():

    total_titles = len(books)

    total_copies = sum(
        book["total_copies"]
        for book in books
    )

    available_copies = sum(
        book["available_copies"]
        for book in books
    )

    borrowed_copies = (
        total_copies - available_copies
    )

    print("\nLIBRARY STATISTICS")
    print("=" * 40)

    print(
        f"Total book titles:      {total_titles}"
    )

    print(
        f"Total book copies:      {total_copies}"
    )

    print(
        f"Available copies:       {available_copies}"
    )

    print(
        f"Currently borrowed:     {borrowed_copies}"
    )

    print(
        f"Total activity records: {len(activity)}"
    )

    # Most borrowed book

    if books:

        most_borrowed = max(
            books,
            key=lambda book: book["times_borrowed"]
        )

        print(
            "\nMost borrowed book:"
        )

        print(
            f"{most_borrowed['title']} "
            f"({most_borrowed['times_borrowed']} times)"
        )

    # Category statistics

    category_counts = {}

    for book in books:

        category = book["category"]

        if category not in category_counts:
            category_counts[category] = 0

        category_counts[category] += 1

    print("\nBooks by category:")

    for category, count in category_counts.items():

        print(
            f"{category}: {count}"
        )

    print("=" * 40)


# --------------------------------------------------
# ADMIN MENU
# --------------------------------------------------

def admin_menu(user):

    while True:

        print("\n" + "=" * 40)
        print("ADMIN MENU")
        print("=" * 40)

        print("1. Display all books")
        print("2. Search books")
        print("3. Add book")
        print("4. Remove book")
        print("5. Sort books")
        print("6. Display categories")
        print("7. Borrowing activity")
        print("8. Statistics")
        print("9. Logout")

        choice = input(
            "\nSelect an option: "
        )

        if choice == "1":
            display_books()
            pause()

        elif choice == "2":
            search_books()
            pause()

        elif choice == "3":
            add_book()
            pause()

        elif choice == "4":
            remove_book()
            pause()

        elif choice == "5":
            sort_books()
            pause()

        elif choice == "6":
            display_categories()
            pause()

        elif choice == "7":
            show_activity()
            pause()

        elif choice == "8":
            show_statistics()
            pause()

        elif choice == "9":
            print("\nLogging out...")
            break

        else:
            print("\nInvalid option.")


# --------------------------------------------------
# USER MENU
# --------------------------------------------------

def user_menu(user):

    while True:

        print("\n" + "=" * 40)
        print(f"USER MENU - {user['username']}")
        print("=" * 40)

        print("1. Display all books")
        print("2. Search books")
        print("3. Borrow book")
        print("4. Return book")
        print("5. My borrowed books")
        print("6. Display categories")
        print("7. Sort books")
        print("8. Logout")

        choice = input(
            "\nSelect an option: "
        )

        if choice == "1":
            display_books()
            pause()

        elif choice == "2":
            search_books()
            pause()

        elif choice == "3":
            borrow_book(user)
            pause()

        elif choice == "4":
            return_book(user)
            pause()

        elif choice == "5":
            display_borrowed_books(user)
            pause()

        elif choice == "6":
            display_categories()
            pause()

        elif choice == "7":
            sort_books()
            pause()

        elif choice == "8":
            print("\nLogging out...")
            break

        else:
            print("\nInvalid option.")


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def login():

    print("\n" + "=" * 45)
    print("LIBRARY MANAGEMENT SYSTEM")
    print("=" * 45)

    username = input("Username: ")
    password = input("Password: ")

    for user in users:

        if (
            user["username"] == username
            and user["password"] == password
        ):

            print(
                f"\nWelcome, {user['username']}!"
            )

            return user

    print("\nIncorrect username or password.")

    return None


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    while True:

        print("\n" + "=" * 45)
        print("PYTHON LIBRARY MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1. Login")
        print("2. Exit")

        choice = input(
            "\nSelect an option: "
        )

        if choice == "1":

            user = login()

            if user:

                if user["role"] == "admin":
                    admin_menu(user)

                else:
                    user_menu(user)

        elif choice == "2":

            print(
                "\nThank you for using the "
                "Library Management System."
            )

            break

        else:

            print(
                "\nInvalid option."
            )


# --------------------------------------------------
# START PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    main()