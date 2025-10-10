from app import db, User
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create invisible admin user (admin@example.com)
        if not User.query.filter_by(username='admin@example.com').first():
            admin_user = User(
                username='admin@example.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✓ Invisible admin user (admin@example.com) created.")
        else:
            print("✓ Invisible admin user (admin@example.com) already exists.")
        
        # Create Grace admin user
        if not User.query.filter_by(username='Grace').first():
            grace_user = User(
                username='Grace',
                password=generate_password_hash('Grace@123'),
                role='admin'
            )
            db.session.add(grace_user)
            db.session.commit()
            print("✓ Grace admin user created.")
        else:
            print("✓ Grace admin user already exists.")
        
        print("\n=== Database initialization complete ===")
        print("Two admin users are ready:")
        print("  1. admin@example.com (invisible in user management)")
        print("  2. Grace (visible admin)")

if __name__ == '__main__':
    from app import app
    init_db()