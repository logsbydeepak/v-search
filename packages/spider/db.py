from dataclasses import dataclass
from nanoid import generate

init_query = """
CREATE TABLE IF NOT EXISTS page (
    url TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    content TEXT
);

CREATE TABLE IF NOT EXISTS ROBOT (
    url TEXT PRIMARY KEY,
    content TEXT
);
"""


@dataclass
class Page:
    url: str
    title: str
    description: str
    content: str


def store_page(db, page: Page):
    db.execute(
        """
        INSERT INTO page (url, title, description, content)
        VALUES (%s, %s, %s, %s);
        """,
        (page.url, page.title, page.description, page.content),
    )
    db.commit()


def retrieve_page(db, url):
    result = db.execute(
        """
        SELECT url, title, description, content FROM page
        WHERE url = %s;
        """,
        (url,),
    )

    row = result.fetchone()
    return Page(*row) if row else None


def store_robot(db, url, content):
    db.execute(
        """
        INSERT INTO robot (url, content)
        VALUES (%s, %s);
        """,
        (url, content),
    )
    db.commit()


def retrieve_robot(db, url):
    result = db.execute(
        """
        SELECT content FROM robot
        WHERE url = %s;
        """,
        (url,),
    )

    row = result.fetchone()
    return row[0] if row else None
