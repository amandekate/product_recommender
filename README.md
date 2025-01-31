## Setup
1. Clone repo: `git clone https://github.com/your-repo.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Populate data: `python scripts/populate_products.py`
5. Start server: `python manage.py runserver`

## API Endpoints
- `GET /api/products/`: List all products
- `POST /api/recommend/`: Get recommendations (payload: `{"product_ids": [1, 2]}`)