from logic import (
    validate_expense,
    calculate_total,
    calculate_average,
    count_expenses,
    calculate_category_totals,
    find_highest_expense,
    calculate_remaining_budget,
    is_over_budget,
)


def test_valid_expense():
    valid, msg = validate_expense("Food", 50, "Eating")
    assert valid == True


def test_invalid_amount():
    valid, msg = validate_expense("Food", -10, "Eating")
    assert valid == False


def test_empty_title():
    valid, msg = validate_expense("", 50, "Eating")
    assert valid == False


def test_calculate_total():
    expenses = [
        {"amount": 10},
        {"amount": 20},
        {"amount": 30},
    ]
    assert calculate_total(expenses) == 60


def test_calculate_average():
    expenses = [
        {"amount": 10},
        {"amount": 20},
        {"amount": 30},
    ]
    assert calculate_average(expenses) == 20


def test_count_expenses():
    expenses = [
        {"amount": 10},
        {"amount": 20},
    ]
    assert count_expenses(expenses) == 2


def test_category_totals():
    expenses = [
        {"category": "Food", "amount": 100},
        {"category": "Food", "amount": 50},
        {"category": "Transport", "amount": 30},
    ]

    result = calculate_category_totals(expenses)

    assert result["Food"] == 150
    assert result["Transport"] == 30


def test_highest_expense():
    expenses = [
        {"title": "Coffee", "amount": 50},
        {"title": "Shoes", "amount": 500},
        {"title": "Bus", "amount": 30},
    ]

    result = find_highest_expense(expenses)

    assert result["title"] == "Shoes"
    assert result["amount"] == 500


def test_remaining_budget():
    assert calculate_remaining_budget(1000, 350) == 650


def test_over_budget_true():
    assert is_over_budget(1000, 1200) == True


def test_over_budget_false():
    assert is_over_budget(1000, 800) == False