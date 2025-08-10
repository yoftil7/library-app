# interactive library app, based on OOP

import json, os


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def borrow(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            print(f"Thank you for borrowing {self.title}")
        else:
            print(f"{self.title} is already borrowed")

    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            print(f"Thank you for returning {self.title}")
        else:
            print(f"{self.title} was not borrowed")

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "available"
        return f"Book: {self.title}, Author: {self.author} - status: {status}"


class Library:
    def __init__(self):
        self.books = []
        self.borrowed_books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"{book.title} is added to library")

    def list_books(self):
        if not self.books:
            print("No books in library")
        for book in self.books:
            print(book)

    def list_available_books(self):
        available_books = [book for book in self.books if not book.is_borrowed]
        if not available_books:
            print("No available books")
        else:
            for book in available_books:
                print(book)
        return available_books

    def list_borrowed(self):
        borrowed_books = [book for book in self.books if book.is_borrowed]
        if not borrowed_books:
            print("No borrowed books")
        else:
            for book in borrowed_books:
                print(book)
        return borrowed_books

    def find_by_author(self, author):
        matches = [book for book in self.books if book.author.lower() == author.lower()]
        if not matches:
            print(f"No books found by '{author}'.")
        else:
            for match in matches:
                print(match)
        return matches

    def borrow_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.borrow()
                return
        print(f"{title} is not found in library")

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                book.return_book()
                return
        print(f"{title} is not found in library")

    def load_books(self, filename="books.json"):
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            print("No library data is avilable to load. file missing or empty")
            return
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for item in data:
                    book = Book(item["title"], item["author"])
                    if item.get("is_borrowed"):
                        book.is_borrowed = True
                    self.books.append(book)
                print("Library is loaded.")
        except FileNotFoundError:
            print("No existing books file found!")

    def save_books(self, filename="books.json"):
        with open(filename, "w") as file:
            data = [
                {"title": b.title, "author": b.author, "is_borrowed": b.is_borrowed}
                for b in self.books
            ]
            if data:
                json.dump(data, file, indent=4)
            else:
                print("Nothing to save")


def menu():
    print("\nhow can we help you today? ")
    print(
        "1. Add book\n2. Borrow book\n3. Return Book\n4. List books\n5. Show available books\n6. List borrowed books\n7. find book by author\n8. exit"
    )


def main():
    lib = Library()
    lib.load_books()

    while True:
        menu()
        choice = input("please choose an option: ").strip()
        print()
        if choice == "1":
            title = input("Book title: ").strip()
            author = input("Author: ").strip()
            b1 = Book(title, author)
            lib.add_book(b1)
        elif choice == "2":
            title = input("Book title: ").strip()
            lib.borrow_book(title)
        elif choice == "3":
            title = input("Book title: ").strip()
            lib.return_book(title)
        elif choice == "4":
            lib.list_books()
        elif choice == "5":
            lib.list_available_books()
        elif choice == "6":
            lib.list_borrowed()
        elif choice == "7":
            author = input("Book author: ").strip()
            lib.find_by_author(author)
        elif choice == "8":
            confirm = input("Are you sure you want to exit (y/n): ").strip().lower()
            if confirm == "y":
                lib.save_books()
                print("exiting app")
                break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
