#!/bin/bash
set -e  # Exit on error

python -m venv --copies /opt/venv
source /opt/venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database and create admin users
echo "Initializing database and creating admin users..."
python init_db.py
echo "Database initialization complete!"

# Run migrations if DATABASE_URL is set (production)
if [ -n "$DATABASE_URL" ]; then
    echo "Running database migrations..."
    flask db upgrade || echo "No migrations to run"
fi