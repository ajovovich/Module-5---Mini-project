
from connect_mysql import connect_database
import re


class Genre:
    def __init__(self):
        self.genre = {}

    def genre_menu(self):
        genre_choice = input("Enter a specific number for the action you'd like to take for Genre Operations:\n1. Add a new genre\n2. View genre details\n3. Display all genres\n")
        if genre_choice == '1':
            self.add_genre()
        elif genre_choice == '2':
            self.view_genre()
        elif genre_choice == '3':
            self.display_genre()
        else:
            print('Please enter a valid choice')

    def add_genre(self):
        try:   
            conn = connect_database()
            cursor = conn.cursor()

            name = input("What genre would you like to add?").lower()
            description = input("Give a brief description of the genre")
            category = input("What is the genre categorized as? (Fiction, Non-Fiction, Poetry etc)")

            if not name or not description or not category:
                print("All fields are required.")
                return

            query = "INSERT INTO Genres (name, description, category) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, description, category))
            conn.commit()
            
            print('A new genre has been added!')
        except Exception as e:
            print('An error has occured: {e}')
        finally:
            cursor.close()
            conn.close()


    def view_genre(self):
        try:
            conn = connect_database()
            cursor = conn.cursor()

            search = input("Enter the name of the genre you'd like to find information about").lower()
            check_query = "SELECT COUNT(*) FROM Genres WHERE name = %s"
            cursor.execute(check_query,(search,))
            result = cursor.fetchone()
            
            if result[0] == 0:
                print(f'Error: The genre: {search} does not exist.')
        
            query = "SELECT * FROM Genres WHERE name = %s"
            cursor.execute(query, (search,))
            genres = cursor.fetchall()
            if genres:   
                for genre in genres:
                    print(f'Here is the information of the genre you are looking for:{genre}')
            else:
                print(f'No information found for the genre "{search}".')
        except Exception as e:
            print(f'An error has occured:{e}')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def display_genre(self):
        try:
            conn = connect_database()
            cursor = conn.cursor()
            query = "SELECT * FROM Genres"
            cursor.execute(query)
            genres = cursor.fetchall()
            if genres:
                for genre in genres:
                    print(f'Here are the genres and their details we have listed: {genre}')
            else:
                print('No genres found.')

        except Exception as e:
            print(f'An error has occurred: {e}')
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

class Author:
    def __init__(self):
        self.author = {}

    def author_menu(self):
        author_choice = input("Enter a specific number for the action you'd like to take for Author Operations:\n1. Add a new author\n2. View author details\n3. Display all authors\n")
        if author_choice == '1':
            self.add_author()
        elif author_choice == '2':
            self.view_author()
        elif author_choice == '3':
            self.display_authors()
        else:
            print('Please enter a valid choice')


    def add_author(self):
        try:
            conn = connect_database()
            cursor = conn.cursor()

            name = input("Who is the author you'd like to add ").strip().lower()
            biography = input("Enter his biography here:").lower()

            if not name or not biography:
                print("Please fill out all fields. If you do not have the biography type 'N/A'")
                return

            query = "INSERT INTO Authors (name, biography) VALUES (%s, %s)"
            cursor.execute(query,(name,biography))
            conn.commit()
            print('The Author and their biography have been added')

        except Exception as e:
            print(f'An error has occured:{e}')
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()



    def view_author(self):
        try:
            conn = connect_database()
            cursor = conn.cursor()

            search = input("Enter the name of the Author you'd like to search for").strip().lower()

            if not search:
                print('Please enter a valid author name.')
                return
        
            query = "SELECT * FROM Authors WHERE name = %s"
            cursor.execute(query, (search,))
            results = cursor.fetchall()

            if results:   
                for author in results:
                    print(f'Here is the information of the Author you are looking for:{author}')
            else:
                print(f'Error: The Author "{search}" does not exist in our database.')

        except Exception as e:
            print(f'An error has occured:{e}')

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def display_authors(self):
        try:
            conn = connect_database()
            cursor = conn.cursor()
            query = "SELECT id, name, biography FROM Authors"
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print('Here are the Authors, their IDs, and their biographies:')
                for author in results:
                    id, name, biography = author
                    print(f'Author ID: {id} | Author: {name} | Biography: {biography}')
            else:
                print('No authors found.')

        except Exception as e:
            print(f'An error has occurred: {e}')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

            
class Book(Genre, Author):
    def __init__(self):
        super().__init__()


    def book_menu(self):
        choice = input("Enter a specific number for the action you'd like to take for Book Operations:\n1. Add a new book\n 2. Borrow a book\n 3. Return a book\n 4. Search for a book\n 5. Display all books")
        if choice == '1':
            self.add_book()
        elif choice == '2':
            self.borrow()
        elif choice == '3':
            self.return_book()
        elif choice == '4':
            self.search()
        elif choice == '5':
            self.display_all()
        else:
            print('Please enter a valid choice')
            
    
    def add_book(self):
        while True:
            try:
                conn = connect_database()
                cursor = conn.cursor()

                title = input("What book would you like to add to the library?").strip()
                author = input('Who is the Author of this book?').strip().lower()
                author_search = ("SELECT id FROM Authors WHERE name = %s")
                cursor.execute(author_search,(author,))
                author_result = cursor.fetchone()
                if not author_result:
                    choice = input('The author does not exist, would you like to add them to our database? (Yes/No)').lower().strip()
                    if choice == 'yes':
                        self.add_author()
                        continue 
                    else:
                        return
                author_id = author_result[0]

                genre = input("What is the genre of this book?")
                genre_search = ('SELECT id FROM Genres WHERE name =%s')
                cursor.execute(genre_search,(genre,))
                genre_result = cursor.fetchone()
                if not genre_result:
                    choice = input('The genre does not exist, would you like to add it to our database? (Yes/No)').lower().strip()
                    if choice == 'yes':
                        self.add_genre()
                        continue
                    else:
                        return
                genre_id = genre_result[0]


                isbn = input("What is ISBN number of this book").strip()
                if not re.match(r'^\d{13}$', isbn):
                    raise ValueError("Invalid ISBN format. Use XXX-XXXXXXXXXX.")
                            
                publication_date = input('When was this book published?').strip()
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', publication_date):
                    raise ValueError("Invalid date format. Use YYYY-MM-DD.")
                
                if not title or not isbn or not publication_date:
                    print("All fields must be filled out")
                    return

                available = True
                query = "INSERT INTO Books (title, author_id, genre_id, isbn, publication_date, availability) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (title, author_id, genre_id, isbn, publication_date, available))
                conn.commit()
                print('The Book and its details have been added!')
                break

            except ValueError as val_err:
                print(f"Input error: {val_err}")

            except Exception as e:
                print(f'An error has occured: {e}')

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
                

    def borrow(self):
        try:    
            conn = connect_database()
            cursor = conn.cursor()
            book_borrow = input("What book would you like to borrow?")

            search_query = "SELECT title, availability FROM Books WHERE title = %s"
            cursor.execute(search_query, (book_borrow,))
            result = cursor.fetchone()
            if not result:
                print("We do not have a book in the database by that name.")
                return
            
            book_title, availability = result
            if not availability:
                print('The book you are looking for is currently unavailable.')
                return
            
            user = input('Enter your library ID here:').strip()
            user_query = "SELECT id FROM Users WHERE library_id = %s"
            cursor.execute(user_query, (user,))
            user_result = cursor.fetchone()
            if not user_result:
                print('Invalid Library ID.')
                return
            user_id = user_result[0]

            book_query = "SELECT id FROM Books WHERE title =%s"
            cursor.execute(book_query, (book_borrow,))
            book_id = cursor.fetchone()[0]

            borrow_date = input('Enter the date you borrowed this book (YYYY-MM-DD): ').strip()
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', borrow_date):
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            
            return_date = input('Enter the date you expect to return this book, note any borrowed time beyond one week will incur late fees (YYYY-MM-DD): ').strip()
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', borrow_date):
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")

            borrowed_query = "INSERT INTO borrowed_books (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(borrowed_query, (user_id, book_id, borrow_date, return_date))
            conn.commit()

            update_query = "UPDATE Books SET availability =%s WHERE title =%s"
            cursor.execute(update_query, (False, book_title))
            conn.commit()

            print(f'You have borrowed "{book_title}".')

        except Exception as e:
            print(f'An error has occured: {e}')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        

    def return_book(self):
        try:    
            conn = connect_database()
            cursor = conn.cursor()
            book_return = input("What book are you returning?").strip()

            search_query = "SELECT title, availability FROM Books WHERE title = %s"
            cursor.execute(search_query, (book_return,))
            result = cursor.fetchone()
            if not result:
                print("We do not have a book in the database by that name.")
                return

            update_query = "UPDATE Books SET availability =%s WHERE title =%s"
            cursor.execute(update_query, (True, book_return))
            conn.commit()

            print(f'You have returned "{book_return}".')

        except Exception as e:
            print(f'An error has occured: {e}')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    

    def search(self):
        try:
            conn = connect_database()
            cursor = conn.cursor()    
            pattern = r'^\d{13}$'
            book_option = input('Would you like to search for a book by its ISBN, Title, Author, Genre?(Input Title/ISBN)').lower()
            book_search_id = ''
            if book_option == 'title':
                book_search = input("Enter the title of the book you are looking for")
                title_query = "SELECT * FROM Books WHERE title = %s"
                cursor.execute(title_query,(book_search,))
                result = cursor.fetchone()

                if result is None:
                    print(f'Error: The book titled: {book_search} does not exist')
                else:
                    print(f'Here are the details for the book you are looking for:{result}')

            elif book_option == 'isbn':
                book_search_id = input('Enter the 13 digit ISBN of the book you are looking for')
                if not re.match(pattern, book_search_id):
                    print('Please enter a valid ISBN number')
                    return
                else:
                    isbn_query = "SELECT * FROM Books WHERE isbn = %s"
                    cursor.execute(isbn_query,(book_search_id,))
                    result = cursor.fetchone()

                if result is None:
                    print(f'Error: The book associated with the ISBN: {book_search_id} does not exist')
                else:
                    print(f'Here are the details for the book you are looking for:{result}')

            elif book_option == 'author':
                author_search = input("Enter the author ID of the books you are looking for: ")
                author_query = "SELECT * FROM Books WHERE author_id = %s"
                cursor.execute(author_query, (author_search,))
                results = cursor.fetchall()

                if not results:
                    print(f'Error: No books found by the author "{author_search}"')
                else:
                    print(f'Here are the books by {author_search}:')
                    for result in results:
                        print(result)

            elif book_option == 'genre':
                genre_search = input("Enter the genre ID of the books you are looking for: ")
                genre_query = "SELECT * FROM Books WHERE genre_id = %s"
                cursor.execute(genre_query, (genre_search,))
                results = cursor.fetchall()

                if not results:
                    print(f'Error: No books found in the genre with ID "{genre_search}"')
                else:
                    print(f'Here are the books in genre ID {genre_search}:')
                    for result in results:
                        print(result)
            else:
                print('Invalid option. Please input "Title", "ISBN", "Author", "Genre".')

        except Exception as e:
            print(f'An error has occured:{e}')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            

    def display_all(self):
        try:
            conn = connect_database()
            cursor = conn.cursor()
            query = "SELECT * FROM Books"
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print("Here are the books and their details we have listed:")
                for book in results:
                    print(book)
            else:
                print('No books found.')

        except Exception as e:
            print(f'An error has occurred: {e}')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()



class User:
    def __init__(self):
        self.users = {}

    def user_menu(self):
        user_choice = input("Enter a specific number for the action you'd like to take for User Operations:\n1. Add a new user\n2. Search for a user\n3. Display all users\n")
        if user_choice == '1':
            self.add_user()
        elif user_choice == '2':
            self.search_user()
        elif user_choice == '3':
            self.display_all_users()
        else:
            print('Please enter a valid choice')


    def add_user(self):
        conn = None
        cursor = None

        try:
            conn = connect_database()
            cursor = conn.cursor()
            pattern = r'^\d{8}$'
            name = input("What is your first and last name?")
            id = input("Enter a random 8 digit number sequence for your Library ID")

            if not name or not id:
                print('All fields are required')
                return
            
            if not re.match(pattern, id):
                print('Please enter a valid 8 digit sequence')
                return

            query = "INSERT INTO Users (name, library_id) VALUES (%s, %s)"
            cursor.execute(query,(name, id))
            conn.commit()
            print('User has been added to the database!')

        except Exception as e:
                print(f'Error has occured:{e}')

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def search_user(self):
        try:
            conn = connect_database()
            cursor = conn.cursor()
            pattern = r'^\d{8}$'

            search = input("Enter the Library ID number associated with the user")

            if not re.match(pattern, search):
                print('Please enter a valid 8 digit sequence for the Library ID')
                return

            check_query = "SELECT COUNT(*) FROM Users WHERE library_id = %s"
            cursor.execute(check_query,(search,))
            result = cursor.fetchone()
            
            if result[0] == 0:
                print(f'Error: The Library ID: {search} does not exist.')
                return
        
            query = "SELECT * FROM Users WHERE library_id = %s"
            cursor.execute(query, (search,))
            results = cursor.fetchall()

            if results:   
                for user in results:
                    print(f'Here is the information of the user associated with the library ID that you are looking for:{user}')
            else:
                print(f'No information found for the Library ID: "{search}".')

        except Exception as e:
            print(f'An error has occured:{e}')

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def display_all_users(self):
        try:
            conn = connect_database()
            cursor = conn.cursor()
            query = "SELECT * FROM Users"
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                print('Here are the Users and their details:')
                for user in results:
                    print(f'User ID: {user[0]} | Name: {user[1]} | Library ID: {user[2]}')
            else:
                print('No Users found.')

        except Exception as e:
            print(f'An error has occurred: {e}')
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


class MainMenu:

    def __init__(self):
        self.book = Book()
        self.user = User()
        self.author = Author()
        self.genre = Genre()


    def start_app(self):
        while True:
            main_choice = input("Welcome to the new Library Management System!\nEnter a specific number to navigate the Main Menu:\n1. Book Operations\n2. User Operations\n3. Author Operations\n4. Genre Operations\n5. Exit\n")
            if main_choice == '1':
                self.book.book_menu()
            elif main_choice == '2':
                self.user.user_menu()
            elif main_choice == '3':
                self.author.author_menu()
            elif main_choice == '4':
                self.genre.genre_menu()
            elif main_choice == '5':
                print("Exiting the Library Management System. Thank you!")
                break
            else:
                print("Please enter a valid choice")

if __name__ == '__main__':
    ui = MainMenu()
    ui.start_app()




        

