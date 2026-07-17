# C$50 Finance — Stock Trading Simulator

A web app that lets users manage a simulated portfolio of stocks: look up real-time quotes, buy and sell shares, and review a full transaction history, all backed by user accounts and a running cash balance.

Built with Python (Flask), Jinja templating, and SQL (SQLite via CS50's `cs50` library), with Bootstrap for layout.

## What it does

- **Register / log in** — accounts are password-protected with hashed credentials (`werkzeug.security`) and enforced password complexity (length, case, digit, special character).
- **Quote** — look up a live price for any ticker symbol via an external stock API.
- **Buy / Sell** — purchase or sell shares at the current quoted price; the app validates input (positive integer shares, sufficient cash or shares on hand) and updates the user's cash balance and holdings transactionally.
- **Portfolio (index)** — aggregates a user's current holdings by symbol, with live valuations and a running grand total.
- **History** — a full log of every buy/sell transaction, with timestamps.

## Structure

```
finance/
├── application.py       # Flask routes: index, buy, sell, quote, history, login, register, logout
├── helpers.py            # apology(), login_required decorator, lookup() (stock API), usd() formatter
├── requirements.txt
├── static/styles.css
└── templates/            # Jinja templates (layout, index, buy, sell, quote, quoted, history, login, register, apology)
```

## Running it

```
pip install -r requirements.txt
export API_KEY=your_stock_api_key
flask run
```

## Origin

Built as my final project for **CS50's Introduction to Computer Science** (Harvard), extending the course's provided Flask/Jinja/SQL skeleton and helper conventions (`apology`, `login_required`) with my own application logic for authentication, transaction handling, balance validation, and portfolio aggregation.
