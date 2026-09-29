# Django Ecommerce Store

A simple ecommerce storefront built with Python and Django, using Bootstrap for styling and SQLite by default for quick setup.

## Features

- Product catalog with category filtering
- Product detail pages
- Shopping cart stored in session
- Checkout form and order creation
- Order confirmation page
- Admin-ready models
- Bootstrap-based storefront design
- Sample product data

## Tech Stack

- Python 3.11+
- Django 5.x
- SQLite (default)
- Bootstrap 5

## Local Setup

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Apply database migrations
5. Seed sample data
6. Run the development server

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## Admin

Create a superuser:

```bash
python manage.py createsuperuser
```

Then log in to:

- http://127.0.0.1:8000/admin/

## Environment Variables

Copy the example file and change values as needed:

```bash
cp .env.example .env
```

## Project Structure

- `storefront/` — Django project settings and URL configuration
- `shop/` — ecommerce app containing models, views, forms, and seed command
- `templates/` — storefront templates
- `static/` — CSS styling

## Next Steps

- Add user authentication and account pages
- Integrate Stripe for payments
- Add wishlist and reviews
- Improve product search and filters
- Use PostgreSQL for production
