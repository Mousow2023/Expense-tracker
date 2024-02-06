# Expense Tracker

#### Video Demo: https://youtu.be/uKpUpaeMJfo?si=6lDFSA5_N-8PeCUK

#### Description:

Expense Tracker is a web application developed as the final project for CS50's Introduction to Computer Science course. This project aims to provide users with a convenient way to manage their personal expenses and gain insights into their spending habits. It allows users to create accounts, log in, and record their expenses, categorizing them for better organization.

### Project Files and Their Functions:
4. **layout.html**
   - A layout template that defines the structure of all pages in the application.
   - It includes the navigation bar, header and a footer.
   - Handles user authentication and navigation links.

7. **register.html**
   - Users can register for an account using this template.
   - They provide a username and password to create an account.
   - Passwords are securely hashed and stored in the database.

5. **login.html**
   - This template provides a login form for users to log in to their accounts.
   - Users enter their username and password to access their expense records.

1. **index.html**
   - This template serves as the homepage of the Expense Tracker application.
   - Provides an option to add a new expense.
   - It displays a list of all expenses recorded by the user, categorized by date.
   - Users can view their total expenses and expenses by category.

2. **add.html**
   - This template is used for adding new expenses to the application.
   - Users can enter the amount, description, date (optional), and select a category for the expense.
   - After submission, the expense is recorded in the database and displayed in the homepage and in the history.

3. **history.html**
   - This template displays the user's expense history.
   - It shows a table with categories, descriptions, amounts, and dates of each recorded expense.

6. **new.html**
   - This template is displayed when the user is new to application and has no recorded expenses.
   - It welcomes the user and suggests adding an expense to get started.

8. **reset.html**
   - Users can reset their password through this template.
   - It requires the old password for verification and asks for a new password and confirmation.
   - Passwords are hashed and updated in the database.

### Design Choices:

- **Bootstrap Framework:** The project uses the Bootstrap framework for styling to ensure a clean and responsive user interface.

- **Jinja2 Templating:** Jinja2 is used for rendering dynamic content in HTML templates, allowing data from the backend to be integrated into the web pages.

- **Password Hashing:** User passwords are securely hashed before being stored in the database, enhancing security.

- **Responsive Layout:** The layout is designed to be responsive, ensuring that the application is accessible on different devices.

#### Technologies Used:
- Python
- Flask
- SQLite
- HTML/CSS
- Jinja2
- CS50 Library

### Acknowledgments:

This project was developed as part of the CS50 course offered by Harvard University. Special thanks to the CS50 staff for their guidance and support.

This WAS CS50!