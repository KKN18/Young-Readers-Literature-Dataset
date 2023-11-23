import json

def clean_and_save_json(input_file, output_file):
    try:
        # Read the JSON file
        with open(input_file, 'r', encoding='utf-8') as file:
            books = json.load(file)

        # Cleaning the data
        cleaned_books = []
        for book in books:
            # Clean the price field only if it doesn't say 'price not found'
            if 'price not found' not in book['price'].lower():
                book['price'] = book['price'].split('$')[1]
            
            # Remove \u200e from book_length, target_age, and dimension
            book['book_length'] = book['book_length'].replace('\u200e', '')
            book['target_age'] = book['target_age'].replace('\u200e', '')
            book['dimension'] = book['dimension'].replace('\u200e', '')

            cleaned_books.append(book)

        # Save the cleaned data back to a new JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(cleaned_books, file, indent=4)

        return "JSON data cleaned and saved successfully."

    except Exception as e:
        return f"An error occurred: {e}"

clean_and_save_json('child_books.json', 'child_books_cleaned.json')