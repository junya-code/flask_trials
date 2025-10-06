from junya_flask import app
from flask import render_template, request, redirect, url_for
import sqlite3
from flask import jsonify

DATABASE = "database.db"


@app.route("/")
def index():
    con = sqlite3.connect(DATABASE)
    db_books = con.execute("SELECT * FROM books").fetchall()
    con.close()

    books = []
    for row in db_books:
        books.append(
            {
                "id": row[0],
                "title": row[1],
                "price": row[2],
                "arrival_day": row[3],
            }
        )

    return render_template("index.html", books=books)


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/register", methods=["POST"])
def register():
    errors = {}

    title = request.form.get("title", "").strip()
    if not title:
        errors["title"] = "タイトルを入力してください"

    # 金額チェック
    try:
        price = int(request.form["price"])
    except (ValueError, TypeError):
        errors["price"] = "金額は数字で入力してください"

    # 年月日チェック
    try:
        year = int(request.form["year"])
        month = int(request.form["month"])
        day = int(request.form["day"])
        if not (1 <= month <= 12 and 1 <= day <= 31):
            errors["date"] = "月または日が不正です"
    except (ValueError, TypeError):
        errors["date"] = "年月日は数字で入力してください"

    if errors:
        return jsonify({"errors": errors}), 400

    arrival_day = f"{year}年{str(month).zfill(2)}月{str(day).zfill(2)}日"

    con = sqlite3.connect(DATABASE)
    con.execute(
        "INSERT INTO books (title, price, arrival_day) VALUES (?, ?, ?)",
        [title, price, arrival_day],
    )
    con.commit()
    con.close()

    return jsonify({"success": True})


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    con = sqlite3.connect(DATABASE)
    con.execute("DELETE FROM books WHERE id = ?", (book_id,))
    con.commit()
    con.close()
    return redirect(url_for("index"))
