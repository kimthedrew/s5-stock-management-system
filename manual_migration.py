#!/usr/bin/env python3
"""
Manual migration script to fix password column length in Neon PostgreSQL database.
Run this script to directly update the database schema.
"""

import os
import psycopg2
from urllib.parse import urlparse

def fix_password_column():
    """Fix the password column length in the database."""
    
    # Get DATABASE_URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not found!")
        return False
    
    try:
        # Parse the DATABASE_URL
        url = urlparse(database_url)
        
        print(f"🔗 Connecting to database: {url.hostname}")
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],  # Remove leading slash
            user=url.username,
            password=url.password,
            sslmode='require'
        )
        
        cur = conn.cursor()
        
        # Check current column type
        cur.execute("""
            SELECT data_type, character_maximum_length 
            FROM information_schema.columns 
            WHERE table_name = 'user' AND column_name = 'password'
        """)
        
        result = cur.fetchone()
        if result:
            current_type, max_length = result
            print(f"📊 Current password column: {current_type}({max_length})")
            
            if max_length and max_length < 255:
                print("🔧 Expanding password column to VARCHAR(255)...")
                
                # Alter the column
                cur.execute('ALTER TABLE "user" ALTER COLUMN password TYPE VARCHAR(255);')
                conn.commit()
                
                print("✅ Password column successfully expanded to 255 characters!")
                
                # Verify the change
                cur.execute("""
                    SELECT data_type, character_maximum_length 
                    FROM information_schema.columns 
                    WHERE table_name = 'user' AND column_name = 'password'
                """)
                
                result = cur.fetchone()
                if result:
                    new_type, new_length = result
                    print(f"✅ Verification: Password column is now {new_type}({new_length})")
                
                return True
            else:
                print("✅ Password column is already large enough!")
                return True
        else:
            print("❌ User table or password column not found!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🚀 Starting manual password column migration...")
    success = fix_password_column()
    if success:
        print("🎉 Migration completed successfully!")
    else:
        print("💥 Migration failed!")
        exit(1)
