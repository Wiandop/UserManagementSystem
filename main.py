from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from html import escape

DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/app"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="Users Management System")
app.mount("/style", StaticFiles(directory="style"), name="style")


def html_page(title: str, body: str) -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <link rel="stylesheet" href="style/style.css">
    </head>
    <body>
        {body}
    </body>
    </html>
    """
    return HTMLResponse(html)


def get_body(users, title: str) -> str:
    rows = "".join(
        f"<tr><td>{escape(str(u['id']))}</td>"
        f"<td>{escape(str(u['login']))}</td>"
        f"<td>{escape(str(u['money_amount']))}</td>"
        f"<td>{escape(str(u['card_number']))}</td></tr>"
        for u in users
    )
    
    return f"""
    <h1>{title}</h1>
    <table>
        <thead><tr><th>ID</th><th>Login</th><th>Money</th><th>Card</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    <p><a href="/">Main Page</a></p>
    """


def error_page(message: str) -> HTMLResponse:
    body = f"<h2>Error</h2><p class='empty'>{escape(message)}</p><p><a href='/'>Main Page</a></p>"
    return html_page("Error", body)


def fetch_all(query: str, **params):
    with SessionLocal() as session:
        return session.execute(text(query), params).mappings().all()


@app.get("/", response_class=HTMLResponse)
def index():
    body = """
    <h1>Users Management System</h1>

    <h3><a href="/users">Active Users List</a></h3>

    <h3>Search by Login</h3>
    <form action="/by-login" method="get">
        <input type="text" name="login" placeholder="Enter login">
        <button type="submit">Search</button>
    </form>
    <p><a href="/by-login?login=admin">Example: admin</a></p>

    <h3>Search by ID</h3>
    <form action="/by-id" method="get">
        <input type="number" name="id" placeholder="Enter ID" min="1">
        <button type="submit">Search</button>
    </form>
    <p><a href="/by-id?id=1">Example: ID 1</a></p>
    """
    return html_page("Main Page", body)


@app.get("/users", response_class=HTMLResponse)
def users_list():
    users = fetch_all(
        "SELECT id, login, money_amount, card_number FROM users WHERE status = 1 ORDER BY id")

    if not users:
        return error_page("No active users")

    return html_page("Users", get_body(users, "Active Users"))


@app.get("/by-login", response_class=HTMLResponse)
def by_login(login: str = Query(..., min_length=1)):
    users = fetch_all(
        "SELECT id, login, money_amount, card_number FROM users WHERE status = 1 AND login = :login",
        login=login,
    )

    if not users:
        return error_page(f"User with login: {escape(login)} not found")

    return html_page(f"User {users[0]['login']}", get_body(users, f"User {users[0]['login']}"))


@app.get("/by-id", response_class=HTMLResponse)
def by_id(id: int = Query(..., ge=1)):
    users = fetch_all(
        "SELECT id, login, money_amount, card_number FROM users WHERE status = 1 AND id = :id",
        id=id,
    )

    if not users:
        return error_page(f"User with ID: {escape(str(id))} not found")

    return html_page(f"User #{users[0]['id']}", get_body(users, f"User #{users[0]['id']}"))
