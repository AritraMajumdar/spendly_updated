# Spendly

> Track every rupee. Own your finances.

Spendly is a personal expense tracker built with Flask. It lets users sign up,
log expenses by category, and see where their money goes through simple
summaries and breakdowns.

This project is a work in progress, built incrementally step by step.

## Tech stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** Jinja2 templates, vanilla CSS & JavaScript
- **Testing:** pytest, pytest-flask

## Project structure

```
expense-tracker/
├── app.py              # Flask app and routes
├── database/
│   ├── __init__.py
│   └── db.py           # DB connection, schema, and seed data
├── static/
│   ├── css/style.css   # Styles
│   └── js/main.js      # Client-side JavaScript
├── templates/
│   ├── base.html        # Shared layout (nav, footer)
│   ├── landing.html      # Marketing/landing page
│   ├── login.html        # Sign in page
│   └── register.html     # Account creation page
└── requirements.txt
```

## Getting started

1. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   python app.py
   ```

   The app runs at [http://localhost:5001](http://localhost:5001).

## Current status

The landing, login, and registration pages are implemented. The following
pieces are still placeholders/in progress:

- [ ] Database setup (`database/db.py`) — connection, schema, seed data
- [ ] User authentication (login, registration, logout, sessions)
- [ ] User profile page
- [ ] Add / edit / delete expenses
- [ ] Expense list, category breakdowns, and date-range filtering
