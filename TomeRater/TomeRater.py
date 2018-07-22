#Import Corner
import re as reg

#Class Corner
#USER CLASS
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        if self.validate_email(address):
            stored_email = self.email
            self.email = address
            return print("Note that the email address has been changed:" \
            "\nStored Email: " + stored_email + "\nNew Email: " + address, end = '\n')
        else:
            return print("Note that the new email address is not valid, please check and try again.")
     
    def __repr__(self):
        return "User: {}\nemail: {}\nbooks read: ".format(self.name, self.email) + str(len(self.books))

    def __eq__(self, other_user):
        return self.email == other_user.email

#enhancement 1 - check mail address before change
    def validate_email(self, address):
        match = reg.match(r'[^@]+@[^@]+\.[^@]+',address)
        if match:
            return True
        else:
            return False
    
    #Book/ User Methods - more methods
    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        rated_books = [rating for rating in self.books.values() if rating]
        return sum(rated_books) / len(rated_books)

#BOOK CLASS
class Book(object):
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        self.price = price
    
    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def get_price(self):
        return self.price    

    def set_isbn(self, new_isbn):
        if isinstance(new_isbn, int): #Making sure that the ISBN only contains numbers and not a string
            stored_isbn = self.isbn
            self.isbn = new_isbn
            return print("Note that the ISBN has been changed:" \
            "\nStored ISBN: " + str(stored_isbn) + "\nNew ISBN: " + str(new_isbn), end = '\n')
        else:
            return print("New ISBN contains invalid characters, please check and retry")    

    def add_rating(self, rating):
        if not isinstance(rating, type(None)):
            if rating >= 0 and rating <= 4:
                return self.ratings.append(rating)
            else:
                return "Invalid Rating - note that the rating can only be between 0 and 4"

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False
    
    def get_average_rating(self):
        total_rating = 0
        for rating in self.ratings:
            total_rating += rating
        return round(total_rating / len(self.ratings), 0)

    def __hash__(self):
        '''Return the hash value of the object (if it has one). 
        Hash values are integers. They are used to quickly compare dictionary keys during a dictionary lookup. 
        Numeric values that compare equal have the same hash value (even if they are of different types, 
        as is the case for 1 and 1.0).'''
        return hash((self.title, self.isbn))    
            

#BOOK SubClass - FICTION
class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{} by {}". format(self.title, self.author)

#BOOK SubClass - Non-Fiction
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level        

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level    

    def __repr__(self):
        return "{}, a {} manual on {}.".format(self.title, self.level, self.subject)

#TomeRater Class - bringing it all together
class TomeRater(object):
    def __init__(self):
       self.users = {}
       self.books = {}

    def create_book(self, title, isbn, price):
        return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price):
        return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price):
        return Non_Fiction(title, subject, level, isbn, price)

    def add_book_to_user(self, book, email, rating = None):
        if email in self.users:
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email, {}!".format(email)) 
    
    def add_user(self, name, email, user_books = None):
        #checking if there is such a user via email, to prevent duplication
        if email in self.users:
            print("Note that we already have this email, {}, on file.".format(email))
        elif "@" not in email:
            print("Note that the email address provided does not contain the @ symbol: {}".format(email))
        else:
            self.users[email] = User(name, email)
            if not isinstance(user_books, type(None)):
                for book in user_books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        for key in self.books.keys():
            print(key)

    def print_users(self):
        for value in self.users.values():
            print(value)

    def most_read_book(self):
        most_read_book_key = None
        most_read = float("-inf")
        for key, value in self.books.items():
            if value > most_read:
                most_read = value
                most_read_book_key = key
        return most_read_book_key

    def highest_rated_book(self):
        highest_rated_book_key = None
        highest_rating = float("-inf")
        for book in self.books.keys():
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
                highest_rated_book_key = book
        return highest_rated_book_key                                

    def most_positive_user(self):
        highest_user = None
        highest_positive_user = float("-inf")
        for user in self.users.values():
            if user.get_average_rating() > highest_positive_user:
                highest_user = user
                highest_positive_user = user.get_average_rating()
        return highest_user

    def __repr__(self):
        return "TomeRater contains: \nUser: {}\nBooks read by users: {}".format(self.users, self.books)    

    def get_n_most_read_books(self, n):
        if n > len(self.books):
            print("Note that the Tome does not contain so many books, and your {} will be adjusted to the max, which is {}."\
            .format(n, len(self.books)))
            n = len(self.books)
        previous_max = float("int")
        output = []
        for index in range(n):
            max_read = float("-int")
            for book, times_read in self.books.items():
                if times_read > max_read and times_read <= previous_max and book not in output:
                    most_book = book
                    max_read = times_read
            output.append(most_book)
            previous_max = max_read
        return output

    def get_n_most_prolific_readers(self, n):
        if n > len(self.users):
            print("Note that the Tome does not contain so many users, and your {} will be adjusted to the max, which is {}."\
            .format(n, len(self.users)))
            n = len(self.users)
        previous_max = float("int")
        output = []
        for index in range(n):
            max_read = float("-int")
            for user in self.users.values():
                if max_read < len(user.books) <= previous_max and user not in output:
                    most_user = user
                    max_read = len(user.books)
            output.append(most_user)
            previous_max = max_read
        return output

    def get_n_most_expensive_books(self, n):
        if n > len(self.books):
            print("Note that the Tome does not contain so many books, and your {} will be adjusted to the max, which is {}."\
            .format(n, len(self.books)))
            n = len(self.books)
        output = []
        for index in range(n):
            max_price = float("-int")
            for book, price in self.books.items():
                if price > max_price and book not in output:
                    max_price = price
                    max_read = book
            output.append(max_read)
        return output      

    def get_worth_of_user(self, user_email):
        total_of_price_of_books = 0
        for email in self.users.items():
            if email == user_email:
                for book in self.books:
                    total_of_price_of_books += book.price
            else:
                print("No such user found with email:  {}".format(user_email))
        return round(total_of_price_of_books, 2)

#testingwork = User("Alan Turing", "alan@turing.com")
#testingbook = Book("Me and I",123456789)
#print(testingbook.isbn)
#new_user = testingwork("Alan Turing", "alan@turing.com")
#print(testingwork.validate_email('email.mail.com'))
#testingwork.change_email("turning.alan@email.com")
#print(testingwork)
#print(testingbook.add_rating(1))
