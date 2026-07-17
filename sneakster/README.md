# Sneakster

A sneaker marketplace/profile app in the spirit of StockX: search a sneaker database, view a detail card for each shoe, and add sneakers to personal Favorites, Wishlist, or Purchased lists — all backed by user accounts.

Built with Python (Flask), Jinja templating, and SQL (SQLite via CS50's `cs50` library), with Bootstrap for layout.

Documentation: Assuming you have all the necessary documents and are operating within the IDE, in your terminal, change directories (cd) into the project and then once again into the folder titled "sneakster." From here, "flask run" and click the link. When you arrive at the site, you will be prompted to login. Register if you don't have an account by clicking register in the top right corner. Or, login if you already have an account. When registering, you will be required to have a capital letter, lowercase letter, number, and symbol in your password. Once you register or login, you will be redirect to the index/home page which showcases your favorite shoes, shoes you wish to purchase, or shoes you have purchased. Initially, this will be empty. But to add to your profile, you can find specific sneakers by searching for them. To search, click on the link in the nav bar that says "Search." Here, you can search for any shoes that are currently in the database. Search keywords from the sneaker's name and all available results will populate. If none of the results are the shoe you were looking for or if it populated zero results, you can navigate to the link that allows you to add to the database. The link can be found at the bottom of the populated search results. To add to the database, you should have the name, description, colorway, style ID, retail price, release date image URL, and a URL to legitimately purchase the real shoe. Input all of this information into the form and your shoe will be appended to the sneaker database. But, this doesn't explain how to add to your profile. In order to do that, you should click on a shoe after you look it up and it will take you to a profile of that shoe. This page will have a description, colorway, style ID, retail price, image, and a URL to purchase the shoe (typically stockX). To add to your lists, there are options at the bottom to do so. Simply select which list you want the shoe to go in, and you can choose multiple (ie. Favorites and Wishlist or Favorites and Purchases). After, the form redirects you to the home page where you will see your work in action. The page displays each respective list -- favorites, wishlist, and purchased sneakers. From this page, just like the search results, you can click on any shoe to see its profile. From the profile page, you can also edit your lists by click edit. Here, you can remove any shoe from your favorites, wishlist, or purchased lists. Next, you can go to Settings by click the link in the nav that says "Settings." Here, you can delete your account should you see fit or change you password. Simply click on the links to do either. When you click change your password, you will be required to input another password still meeting all the requirements. You'll then be logged out and must log back in to access your profile. Then, to delete your account. It will take you to a form to verify that this is decision you want to make. Click "yes" and your account will be deleted accordingly. Other than that, the final feature is simply to log out. If you click the log out link at the top, you will be logged out and must relog to see your profile again.

## Structure

```
sneakster/
├── application.py       # Flask routes: index, search, shoe, add, append, edit, settings, change, delete, login, register, logout
├── helpers.py             # apology(), login_required decorator, usd() formatter
├── requirements.txt
├── static/styles.css
├── templates/             # Jinja templates (layout, index, search, searched, nonexistent, shoe, add, edit, settings, change, delete, login, register, apology)
└── DESIGN.md              # original write-up of the SQL schema and route-by-route design decisions
```

## Running it

```
pip install -r requirements.txt
flask run
```

## Origin

Built as a personal final project for **CS50's Introduction to Computer Science** (Harvard), extending the course's provided Flask/Jinja/SQL skeleton and helper conventions (`apology`, `login_required`) with original schema design (`users`, `sneakers`, `profile` tables) and application logic for search, profile management, and list curation. No sneaker-market API access was available at the time (see `DESIGN.md`), so the catalog was seeded manually and the `/add` route was built to let the database grow over time.
