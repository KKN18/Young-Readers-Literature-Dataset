# First, I'll load the content of both files to understand their formats and how they differ.

file_path_books_data = '/root/kinam/Children-Book-Dataset/goodreads/books_data.json'
file_path_yes24_books_data = '/root/kinam/Children-Book-Dataset/yes24/yes24_books_data.json'

# Reading the content of the files
with open(file_path_books_data, 'r') as file:
    books_data_content = file.read()

with open(file_path_yes24_books_data, 'r') as file:
    yes24_books_data_content = file.read()

# Displaying the first 500 characters of each file to understand their structure
preview_books_data = books_data_content[:500]
preview_yes24_books_data = yes24_books_data_content[:500]

preview_books_data, preview_yes24_books_data
