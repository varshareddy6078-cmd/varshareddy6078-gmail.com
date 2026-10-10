
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage for expenses
expenses = []
next_id = 1


@app.route("/")
def home():
    total = sum(expense["amount"] for expense in expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


@app.route("/add", methods=["POST"])
def add_expense():
    global next_id

    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    date = request.form.get("date", "").strip()

    try:
        amount = float(request.form.get("amount", 0))
    except ValueError:
        return "Please enter a valid amount.", 400

    if not title or not category or not date or amount <= 0:
        return "Please enter valid expense details.", 400

    expenses.append({
        "id": next_id,
        "title": title,
        "category": category,
        "amount": amount,
        "date": date
    })

    next_id += 1

    return redirect(url_for("home"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    expenses[:] = [
        expense for expense in expenses
        if expense["id"] != expense_id
    ]

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
