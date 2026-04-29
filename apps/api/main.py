from flask import Flask, request, jsonify, g
import os
import tkz
import psycopg

app = Flask(__name__)

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise Exception("Missing DB_URL")


def get_db():
    if "db" not in g:
        g.db = psycopg.connect(DB_URL)
    return g.db


@app.get("/search")
def hello_world():
    result = []
    query = request.args.get("q", "")
    if not query:
        return jsonify(result)

    words = tkz.tokenize(query)

    db = get_db()

    rows = db.execute(
        """
        SELECT
            p.url,
            p.title,
            p.description,
            SUM(w.frequency) AS keyword_score,
            COUNT(pl.from_url) AS backlinks,
            SUM(w.frequency) + COUNT(pl.from_url) AS total_score
        FROM word_index w
        JOIN page p ON p.id = w.page_id
        LEFT JOIN page_link pl ON pl.to_url = p.url
        WHERE w.word = ANY(%s)
        GROUP BY p.id, p.url, p.title
        ORDER BY total_score DESC
        LIMIT 10;
        """,
        (words,),
    ).fetchall()

    for row in rows:
        result.append(
            {"url": row["url"], "title": row["title"], "description": row["title"]}
        )

    return result
