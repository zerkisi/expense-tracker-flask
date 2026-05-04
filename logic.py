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