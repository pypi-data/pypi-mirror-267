from book import Book
from user import User


def main():
    books = []
    users = []

    while True:
        print("\nWelcome to the Library Management System")
        print("----------------------------------------")
        print("1. Add a new book")
        print("2. Display all books")
        print("3. Add a new user")
        print("4. Display all users")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            isbn = input("Enter the ISBN of the book: ")
            books.append(Book(title, author, isbn))
            print("Book added successfully!")

        elif choice == "2":
            print("\nList of all books:")
            for book in books:
                print(book)

        elif choice == "3":
            user_id = input("Enter the user ID: ")
            name = input("Enter the user's name: ")
            email = input("Enter the user's email: ")
            users.append(User(user_id, name, email))
            print("User added successfully!")

        elif choice == "4":
            print("\nList of all users:")
            for user in users:
                print(user)

        elif choice == "5":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
