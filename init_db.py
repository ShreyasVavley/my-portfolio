from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    # Explicitly create the Shreyas user
    if not User.query.filter_by(username='Shreyas').first():
        hashed_pw = generate_password_hash('Shreyas@22')
        new_user = User(username='Shreyas', password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        print("Database created and User 'Shreyas' initialized!")