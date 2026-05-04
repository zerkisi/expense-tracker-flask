\# FinTrack - Personal Expense Tracker



FinTrack is a multi-user expense tracking web application built with Flask and raw SQL.



\## Features



\- User registration, login, logout

\- Session-based authentication

\- Multi-user data isolation

\- Add, view, edit, and delete expenses

\- Search expenses by title or note

\- Filter expenses by:

&#x20; - Category

&#x20; - Date range

&#x20; - Payment method

&#x20; - Payment status

&#x20; - Recurring / non-recurring

\- Monthly budget tracking

\- Budget warning

\- Category summary

\- Spending chart

\- Highest expense summary

\- CSV export

\- Profile page

\- Change password

\- Forgot password

\- Strong password validation

\- Dark mode

\- Landing page



\## Technologies



\- Python

\- Flask

\- SQLite

\- Raw SQL

\- HTML

\- CSS

\- JavaScript

\- Chart.js

\- Pytest



\## Database



The application uses two main tables:



\- users

\- expenses



Each expense is linked to a user using `user\_id`.



\## User Stories



\### \[US1] Add Expense



As a user, I want to add an expense so that I can track my spending.



Acceptance Criteria:

\- User must be logged in.

\- User can enter title, amount, category, date, payment method, status, recurring option, and note.

\- Amount must be greater than 0.

\- Expense is saved with the logged-in user's ID.



\### \[US2] Edit Expense



As a user, I want to edit my own expenses so that I can correct or update my records.



Acceptance Criteria:

\- User must be logged in.

\- User can edit only their own expense.

\- Updated data is saved correctly.

\- Invalid amount is rejected.



\### \[US3] Delete Expense



As a user, I want to delete my own expenses so that I can remove incorrect records.



Acceptance Criteria:

\- User must be logged in.

\- User can delete only their own expense.

\- Deleted expense is removed from the dashboard.



\### \[US4] Search and Filter Expenses



As a user, I want to search and filter my expenses so that I can analyze my spending easily.



Acceptance Criteria:

\- User can search by title or note.

\- User can filter by category.

\- User can filter by date range.

\- User can filter by payment method.

\- User can filter by payment status.

\- User can filter recurring and non-recurring expenses.



\### \[US5] View Spending Summary



As a user, I want to view summaries of my spending so that I can understand my financial behavior.



Acceptance Criteria:

\- Dashboard shows total spending.

\- Dashboard shows average expense.

\- Dashboard shows number of expenses.

\- Dashboard shows highest expense.

\- Dashboard shows top category.

\- Dashboard shows category chart.

\- Dashboard shows monthly budget and remaining budget.

\- User receives a warning if spending exceeds budget.



\## How to Run



```bash

pip install -r requirements.txt

flask --app app init-db

flask --app app run

