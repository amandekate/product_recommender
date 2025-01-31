# Django-Based Product Recommendation Engine with Analytics Dashboard

## Problem Statement
Build a system that:
1. Stores product/order data
2. Provides CRUD operations via API
3. Recommends products based on purchase history
4. Visualizes product relationships

## Solution Approach
- **Models**: Product, Order (with OrderItem through-model)
- **APIs**: RESTful endpoints for CRUD operations
- **Recommendation**: Frequency-based collaborative filtering
- **Dashboard**: Chart.js visualizations for product analytics

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/product-recommender.git
cd product-recommender
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies 
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file with the following content:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup 
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Populate Sample Data 
```bash
python scripts/populate_products.py  # 20 sample products
python scripts/populate_orders.py    # 10 sample orders
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## API Endpoints

| Endpoint          | Method | Description                  |
|------------------|--------|------------------------------|
| `/api/products/`  | GET    | List all products           |
| `/api/products/`  | POST   | Create new product          |
| `/api/recommend/` | POST   | Get recommendations         |
| `/api/dashboard/` | GET    | Analytics dashboard         |

### Example Recommendation Request:
```bash
curl -X POST http://localhost:8000/api/recommend/ \
  -H "Content-Type: application/json" \
  -d '{"product_ids": [1, 3]}'
`````

#### Sample Response:
```json
[
  {
    "id": 5,
    "name": "Wireless Headphones",
    "price": "149.99",
    "category": "Electronics"
  },
  {
    "id": 2,
    "name": "Bluetooth Speaker",
    "price": "89.99",
    "category": "Electronics"
  }
]
