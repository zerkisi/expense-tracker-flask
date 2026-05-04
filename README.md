# FinTrack - Personal Expense Tracker

FinTrack is a multi-user expense tracking web application built with Flask and raw SQL.  
It allows users to manage their expenses, analyze spending, and track budgets.

---

## Features

- User registration, login, logout
- Session-based authentication
- Multi-user data isolation

### Expense Management
- Add, view, edit, and delete expenses
- Each expense includes:
  - Title
  - Amount
  - Category
  - Date
  - Payment method
  - Status (Paid / Pending)
  - Recurring option
  - Note

### Filtering & Search
- Search expenses by title or note
- Filter expenses by:
  - Category
  - Date range
  - Payment method
  - Payment status
  - Recurring / non-recurring

### Analytics & Dashboard
- Total spending
- Average expense
- Expense count
- Highest expense
- Top category
- Category summary
- Spending chart (Chart.js)

### Budget System
- Monthly budget tracking
- Remaining budget calculation
- Warning when budget is exceeded

### Additional Features
- CSV export
- Profile page
- Change password
- Forgot password
- Strong password validation
- Dark mode
- Landing page

---

## Technologies

- Python
- Flask
- SQLite
- Raw SQL
- HTML / CSS / JavaScript
- Chart.js
- Pytest

---

## Database

The application uses two main tables:

- `users`
- `expenses`

Each expense is linked to a user using `user_id`.

---

## User Stories

### [US1] Add Expense
As a user, I want to add an expense so that I can track my spending.

**Acceptance Criteria:**
- User must be logged in
- User can enter title, amount, category, date
- User can select payment method and status
- User can mark expense as recurring
- Amount must be greater than 0
- Expense is saved with the logged-in user

---

### [US2] Edit Expense
As a user, I want to edit my expenses so that I can update incorrect data.

**Acceptance Criteria:**
- User must be logged in
- User can only edit their own expenses
- Updated values are saved correctly
- Invalid amount is rejected

---

### [US3] Delete Expense
As a user, I want to delete my expenses so that I can remove incorrect records.

**Acceptance Criteria:**
- User must be logged in
- User can only delete their own expenses
- Expense is removed from the system

---

### [US4] Search and Filter Expenses
As a user, I want to search and filter my expenses so that I can analyze my spending.

**Acceptance Criteria:**
- Search by title or note
- Filter by category
- Filter by payment method
- Filter by status
- Filter by recurring
- Filter by date range

---

### [US5] View Spending Summary
As a user, I want to view summaries so that I can understand my financial behavior.

**Acceptance Criteria:**
- Dashboard shows total spending
- Dashboard shows average expense
- Dashboard shows expense count
- Dashboard shows highest expense
- Dashboard shows top category
- Dashboard shows category chart
- Dashboard shows monthly budget
- Warning appears if budget is exceeded

---

## How to Run

```bash
pip install -r requirements.txt
flask --app app init-db
flask --app app run
