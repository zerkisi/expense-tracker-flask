def validate_expense(title, amount, category):
    if not title or title.strip() == "":
        return False, "Title cannot be empty"

    try:
        amount = float(amount)
        if amount < 100:
            return False, "Amount must be at least 100"
    except:
        return False, "Invalid amount"

    if not category or category.strip() == "":
        return False, "Category cannot be empty"

    return True, "Valid"


def calculate_total(expenses):
    total = 0
    for exp in expenses:
        total += exp["amount"]
    return total


def calculate_average(expenses):
    if len(expenses) == 0:
        return 0
    return calculate_total(expenses) / len(expenses)


def count_expenses(expenses):
    return len(expenses)


def calculate_category_totals(expenses):
    category_totals = {}

    for exp in expenses:
        category = exp["category"]
        amount = exp["amount"]

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += amount

    return category_totals


def find_highest_expense(expenses):
    if len(expenses) == 0:
        return None

    highest = expenses[0]

    for exp in expenses:
        if exp["amount"] > highest["amount"]:
            highest = exp

    return highest


def find_top_category(category_totals):
    if len(category_totals) == 0:
        return None

    top_category = None
    top_amount = 0

    for category, amount in category_totals.items():
        if amount > top_amount:
            top_category = category
            top_amount = amount

    return {
        "category": top_category,
        "amount": top_amount
    }


def calculate_remaining_budget(monthly_budget, total_spending):
    return monthly_budget - total_spending


def is_over_budget(monthly_budget, total_spending):
    if monthly_budget <= 0:
        return False
    return total_spending > monthly_budget

import re

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not re.search(r"[A-Z]", password):
        return False, "Must include uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Must include lowercase letter"

    if not re.search(r"[0-9]", password):
        return False, "Must include number"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Must include special character"

    return True, "Valid"