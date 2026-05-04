def validate_expense(title, amount, category):
    if not title or title.strip() == "":
        return False, "Title cannot be empty"

    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than 0"
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