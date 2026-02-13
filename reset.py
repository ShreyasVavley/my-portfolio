from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Step 1: Create the tables if they don't exist
    db.create_all()
    
    # Step 2: Now look for the user 'Shreyas'
    user = User.query.filter_by(username='Shreyas').first()
    
    if user:
        user.password = generate_password_hash('Shreyas@22')
        db.session.commit()
        print("Password updated successfully for Shreyas!")
    else:
        # Create the user if they don't exist
        new_user = User(username='Shreyas', password=generate_password_hash('Shreyas@22'))
        db.session.add(new_user)
        db.session.commit()
        print("User 'Shreyas' created successfully with your password.")