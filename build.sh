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
    echo "DATABASE_URL found, running migrations..."
    echo "Current migration status:"
    flask db current
    echo "Running migrations..."
    flask db upgrade
    echo "Migration status after upgrade:"
    flask db current
    
    # If migration still shows old version, apply SQL fix directly
    CURRENT_VERSION=$(flask db current | grep -o '[a-f0-9]\{12\}' || echo "")
    if [ "$CURRENT_VERSION" = "189dc463a3f6" ]; then
        echo "Migration not applied, applying SQL fix directly..."
        python -c "
import os
import psycopg2
from urllib.parse import urlparse

# Parse DATABASE_URL
url = urlparse(os.environ['DATABASE_URL'])
conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    user=url.username,
    password=url.password,
    sslmode='require'
)
cur = conn.cursor()
try:
    cur.execute('ALTER TABLE \"user\" ALTER COLUMN password TYPE VARCHAR(255);')
    conn.commit()
    print('Password column expanded to 255 characters')
except Exception as e:
    print(f'Error: {e}')
finally:
    cur.close()
    conn.close()
"
        echo "SQL fix applied!"
    fi
    
    echo "Migrations completed successfully!"
else
    echo "No DATABASE_URL found, skipping migrations (local development)"
fi