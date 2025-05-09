import sqlite3
from pathlib import Path
from flask import Flask, render_template


app = Flask(__name__)


def get_db_connection():
    db = Path(__file__).parent / "peldet.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/peldetaji")
def products():
    conn = get_db_connection()
    peldetajs = conn.execute("SELECT * FROM peldetaji").fetchall()
    conn.close()
    return render_template("peldetaji.html", peldetajs=peldetajs)


@app .route ("/ <int:peldetajs_id>")
def peldetaji_show(peldetajs_id):
    conn = get_db_connection ()
    peldetajs = conn.execute(
        """
        SELECT "peldetaji".*, "disciplinas"."vards" AS "disciplina", "distances"."metri" AS "distance", "regioni"."vards" AS "valsts"
        FROM peldetaji
        LEFT JOIN "disciplinas" ON "peldetaji"."disciplina_id" = "disciplinas"."id"
        LEFT JOIN "distances" ON "peldetaji"."distance_id" = "distances"."id"
        LEFT JOIN "regioni" ON "peldetaji"."regions_id" = "regioni"."id"
        WHERE "peldetaji"."id" = ?
        """,
        (peldetajs_id,),
    ).fetchone()
    conn. close ()
    return render_template ("peldetaji_info.html", peldetajs=peldetajs)


if __name__ == "__main__":
    app.run(debug=True)
