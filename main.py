import json
import os
import tkinter as tk
from tkinter import messagebox

def add_book(lib, title, author, year):
    id = len(lib) + 1
    lib.append({"id": id, "title": title, "author": author, "year": year})

def display_book(lib):
    for book in lib:
        print(f"Id: {book['id']}, Title: {book['title']}, Author: {book['author']}, Year: {book['year']}")

def remove_book(lib, id):
    found = False
    for book in lib:
        if book['id'] == id:
            lib.remove(book)
            found = True
            print("Book with ID {id} has been removed.")
            break
    if not found:
        print("Book not found.")

def get_user_confirmation(lib, book_title, book_author, book_year):
    while True:
        print("You want to add a book - " + book_title + " by " + book_author + " written in " + str(book_year))
        print("Press:\n1 - add book\n2 - change data\n3 - abandon the changes")
        try:
            add_option = int(input("Your choice is: "))
            if add_option == 1:
                add_book(lib, book_title, book_author, book_year)
                print("Book added")
                break
            elif add_option == 2:
                book_title, book_author, book_year = edit_book_data(book_title, book_author, book_year)
            elif add_option == 3:
                print("Changes abandoned.")
                break
            else:
                print("Invalid option, please choose 1, 2, or 3.")
        except ValueError:
            print("You have to choose and it must be a number!")

def edit_book_data(book_title, book_author, book_year):
    print("Which one you want to edit?\n1 - title\n2 - author\n3 - year\n4 - go back")
    edit_option = int(input("Type edit option: "))
    if edit_option == 1:
        book_title = input("Type book title: ").strip()
        if not book_title:
            print("Title is required.")
    elif edit_option == 2:
        book_author = input("Type book author: ").strip()
        if not book_author:
            print("Author is required.")
    elif edit_option == 3:
        while True:
            try:
                book_year = int(input("Type book year: "))
                if book_year > 2024 or book_year < 0:
                    print("Incorrect year for this book")
                else:
                    break
            except ValueError:
                print("Year must be a number")
    return book_title, book_author, book_year

def load_library_from_file(filename='save_lib.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return []

def search_books(lib):
    search_query = input("Enter search query (title, author, or year): ").strip()
    found_books = []

    try:
        search_query = int(search_query)
        search_field = 'year'
    except ValueError:
        search_field = 'text'

    for book in lib:
        if search_field == 'year':
            if book['year'] == search_query:
                found_books.append(book)
        else:
            if search_query.lower() in book['title'].lower() or search_query.lower() in book['author'].lower():
                found_books.append(book)
    
    if found_books:
        print("Found books:")
        for book in found_books:
            print(f"Id: {book['id']}, Title: {book['title']}, Author: {book['author']}, Year: {book['year']}")
    else:
        print("No books found matching the query.")

def add_book_gui():
    title = title_entry.get()
    author = author_entry.get()
    try:
        year = int(year_entry.get())
        if year > 2024 or year < 0:
            raise ValueError("Year out of range.")
        add_book(lib, title, author, year)
        messagebox.showinfo("Success", "Book added successfully")
    except ValueError as e:
        messagebox.showerror("Error", "Invalid year. Please enter a correct year.")

lib = []
print("Choose one option\n1 - add book\n2 - display books\n3 - remove book\n4 - save library\n5 - load library\n6 - search from lib\n7 - exit")
while True:
    try:
        option = int(input("Type: "))
        if option == 1:
            book_title = input("Type book title: ").strip()
            book_author = input("Type book author: ").strip()
            book_year = int(input("Type book year: "))
            get_user_confirmation(lib, book_title, book_author, book_year)
        elif option == 2:
            display_book(lib)
        elif option == 3:
            remove_option = int(input("Type id book for remove: "))
            remove_book(lib, remove_option)
        elif option == 4:
            with open('save_lib.json', 'w') as save_lib_file:
                json.dump(lib, save_lib_file)
            print("Library saved successfully.")
        elif option == 5:
            lib = load_library_from_file()
            print("Loaded library from file.")
        elif option == 6:
            search_books(lib)
        elif option == 7:
            print("See you soon!")
            break
        else:
            print("Invalid option, please choose a valid one.")
    except ValueError:
        print("Invalid input, please enter a number.")


root = tk.Tk()
root.title("Library Management")

tk.Label(root, text="Book Title:").grid(row=0)
tk.Label(root, text="Author:").grid(row=1)
tk.Label(root, text="Year:").grid(row=2)

title_entry = tk.Entry(root)
author_entry = tk.Entry(root)
year_entry = tk.Entry(root)

title_entry.grid(row=0, column=1)
author_entry.grid(row=1, column=1)
year_entry.grid(row=2, column=1)


add_button = tk.Button(root, text="Add Book", command=add_book_gui)
add_button.grid(row=3, column=1)

root.mainloop()