import os  # Required for hosting environment variables
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from models import db, User, Project, Message, About, LoginLog

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shreyas_secret_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    projects = Project.query.filter_by(is_visible=True).all()
    about = About.query.first()
    return render_template('index.html', projects=projects, about=about)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            # Security Log
            new_log = LoginLog(ip_address=request.remote_addr)
            db.session.add(new_log)
            db.session.commit()
            login_user(user)
            return redirect(url_for('admin'))
        flash('Invalid Credentials')
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        new_project = Project(
            title=request.form['title'],
            description=request.form['description'],
            tech_stack=request.form['tech_stack'],
            link=request.form['link']
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('admin'))
    
    return render_template('admin.html', 
                           projects=Project.query.all(), 
                           about=About.query.first(),
                           logs=LoginLog.query.order_by(LoginLog.timestamp.desc()).limit(5).all(),
                           messages=Message.query.order_by(Message.timestamp.desc()).all())

@app.route('/admin/about', methods=['POST'])
@login_required
def update_about():
    about = About.query.first()
    if about:
        about.content = request.form['content']
    else:
        db.session.add(About(content=request.form['content']))
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/message/delete/<int:id>')
@login_required
def delete_message(id):
    msg = db.session.get(Message, id)
    if msg:
        db.session.delete(msg)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
@login_required
def delete_project(id):
    p = db.session.get(Project, id)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect(url_for('admin'))
@app.route('/contact', methods=['POST'])
def contact():
    new_msg = Message(
        name=request.form['name'],
        email=request.form['email'],
        content=request.form['content']
    )
    db.session.add(new_msg)
    db.session.commit()
    flash("Message sent successfully!")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # This logic allows Render to set the port, or defaults to 5000 for local use
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)