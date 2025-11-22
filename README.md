# Django Pluggable Rule Engine

A Django project implementing a pluggable rule engine for order validation.

## Features

- **Order Model**: Simple model with `total` and `items_count` fields
- **Pluggable Rule Engine**: Auto-registration system for rules
- **REST API**: Django REST Framework endpoint for rule checking
- **Pre-built Rules**: Three example rules included

## Models

### Order
- `total`: DecimalField (max_digits=10, decimal_places=2)
- `items_count`: IntegerField

## Rules

Rules are automatically registered when defined. Each rule inherits from `BaseRule` and implements a `check(order)` method.

### Available Rules

1. **min_total_100**: Order total > 100
2. **min_items_2**: Order items_count >= 2
3. **divisible_by_5**: Order total is divisible by 5

### Adding New Rules

```python
class CustomRule(BaseRule):
    name = "custom_rule"

    def check(self, order):
        # Your logic here
        return True  # or False
```

## API Endpoint

### POST /rules/check/

**Request:**
```json
{
  "order_id": 1,
  "rules": ["min_total_100", "min_items_2"]
}
```

**Response:**
```json
{
  "passed": true,
  "details": {
    "min_total_100": true,
    "min_items_2": true
  }
}
```

## Local Setup

1. Create project directory and virtual environment:
```bash
cd Desktop/
mkdir rule_folder
cd rule_folder
python3 -m venv revenv
source revenv/bin/activate
python -m pip install --upgrade pip
```

2. Clone project and install dependencies:
```bash
git clone git@github.com:Jaye-python/engine_project.git
cd engine_project
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Seed sample data:
```bash
python manage.py seed_orders
```

5. Run tests:
```bash
python manage.py test
```

6. Start server:
```bash
python manage.py runserver
```

## Sample Data

The project includes 3 sample orders:
- Order 1: $150.00, 3 items
- Order 2: $75.50, 1 item
- Order 3: $200.00, 5 items

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Demo

Run the demo script to see the rule engine in action:
```bash
python demo.py
```
