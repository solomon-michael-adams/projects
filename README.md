# Solomon Adams — Programming Projects

Two full-stack Python web apps, originally built as coursework and reconstructed here from graded submission records for portfolio purposes.

## [`finance/`](./finance) — C$50 Finance

A simulated stock-trading platform: real-time quote lookups, buy/sell with balance validation, and full transaction history, on user accounts with hashed passwords.

## [`sneakster/`](./sneakster) — Sneakster

A StockX-style sneaker marketplace/profile app: search a sneaker catalog, view detail cards, and curate personal Favorites / Wishlist / Purchased lists, on user accounts with hashed passwords. See [`sneakster/DESIGN.md`](./sneakster/DESIGN.md) for the original schema write-up and design rationale.

## Stack

Python, Flask, Jinja, SQL (SQLite), Bootstrap.

## A note on origin

Both projects were built as final projects for **Harvard's CS50: Introduction to Computer Science**, which provides a starting Flask/Jinja/SQL skeleton and a small set of helper conventions (`apology()`, `login_required()`) used across student projects. The database schema, route logic, validation rules, and feature set in each project are my own design and implementation. Source was reconstructed from my original graded submission records (Gradescope exports), since the working repositories were not preserved online at the time; a couple of copy/paste artifacts from that export were cleaned up, but the logic is unchanged from what was submitted and graded.
