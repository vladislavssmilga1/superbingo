import sqlite3
from pathlib import Path
from flask import Flask, render_template


app = Flask(__name__)


def get_db_connection():
    db = Path(__file__).parent / "miniveikalins.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/peldetaji")
def products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM peldetaji").fetchall()
    conn.close()
    return render_template("peldetaji.html", products=products)


@app .route ("/ <int:peldetajs_id>")
def peldetaji_show(product_id):
    conn = get_db_connection ()
    peldetajs = conn.execute(
        """
        SELECT "products".*, "producers"."name" AS "producer"
        FROM products
        LEFT JOIN "producers" ON "products"."producer_id" = "producers"."id"
        WHERE "products"."id" = ?
        """,
        (product_id,),
    ).fetchone()
    conn. close () # Aizver savienojumu ar datubāzi
    return render_template ("peldetaji_info.html", peldetajs=peldetajs)


if __name__ == "__main__":
    app.run(debug=True)
