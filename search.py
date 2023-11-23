import json
import tkinter as tk
from tkinter import scrolledtext

def search_books(query):
    try:
        with open('book_information.json', 'r', encoding='utf-8') as file:
            books = json.load(file)

        matching_books = [book for book in books if query.lower() in book['name'].lower()]

        return matching_books
    except FileNotFoundError:
        return []

def on_search_click():
    search_query = entry.get()
    result = search_books(search_query)

    output_text.delete(1.0, tk.END)

    if result:
        output_text.insert(tk.END, f"Found matching books for '{search_query}':\n")
        for book in result:
            output_text.insert(tk.END, f"Name: {book['name']}, Author: {book['author']}\n")
    else:
        output_text.insert(tk.END, f"No matching books found for '{search_query}'\n")

root = tk.Tk()
root.title("Book Search")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

search_button = tk.Button(root, text="Search", command=on_search_click)
search_button.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD)
output_text.pack(pady=10)

root.mainloop()
