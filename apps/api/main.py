from time import perf_counter

from flask import Flask, request, jsonify, g
from psycopg.rows import dict_row
from db import close_db, get_db
import tkz

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 50

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


@app.teardown_appcontext
def teardown_db(exception):
    close_db(g)


@app.get("/search")
def hello_world():
    started_at = perf_counter()
    query = request.args.get("q", "")
    page = max(request.args.get("page", default=1, type=int) or 1, 1)
    page_size = request.args.get("page_size", default=DEFAULT_PAGE_SIZE, type=int)
    page_size = min(max(page_size or DEFAULT_PAGE_SIZE, 1), MAX_PAGE_SIZE)

    if not query:
        return jsonify(
            {
                "results": [],
                "meta": {
                    "query": query,
                    "search_speed_ms": round((perf_counter() - started_at) * 1000, 2),
                    "total_results": 0,
                },
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_pages": 0,
                    "has_next": False,
                    "has_previous": False,
                },
            }
        )

    words = tkz.tokenize(query)

    db = get_db(g, row_factory=dict_row)

    rows = db.execute(
        """
        SELECT
            p.url,
            p.title,
            p.description,
            SUM(w.frequency) AS keyword_score,
            COUNT(pl.from_url) AS backlinks,
            SUM(w.frequency) + COUNT(pl.from_url) AS total_score
        FROM quickly_word_index w
        JOIN quickly_page p ON p.id = w.page_id
        LEFT JOIN quickly_page_link pl ON pl.to_url = p.url
        WHERE w.word = ANY(%s)
        GROUP BY p.id, p.url, p.title, p.description;
        """,
        (words,),
    ).fetchall()

    sorted_rows = sorted(
        rows,
        key=lambda row: (
            row["total_score"] or 0,
            row["keyword_score"] or 0,
            row["backlinks"] or 0,
            row["title"] or "",
        ),
        reverse=True,
    )
    total_results = len(sorted_rows)
    total_pages = (total_results + page_size - 1) // page_size
    if total_pages:
        page = min(page, total_pages)
    start = (page - 1) * page_size
    end = start + page_size

    results = []
    for row in sorted_rows[start:end]:
        results.append(
            {
                "url": row["url"],
                "title": row["title"],
                "description": row["description"],
                "score": row["total_score"],
            }
        )

    return jsonify(
        {
            "results": results,
            "meta": {
                "query": query,
                "search_speed_ms": round((perf_counter() - started_at) * 1000, 2),
                "total_results": total_results,
            },
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            },
        }
    )
