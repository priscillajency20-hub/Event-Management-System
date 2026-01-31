from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from config import Config
from models import db, Admin, Event, Guest
import qrcode
import io
import uuid

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# --- SETUP COMMAND ---
# Run this ONCE to create tables: python app.py setup
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'setup':
    with app.app_context():
        db.create_all()
        if not Admin.query.filter_by(username='admin').first():
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = Admin(username='admin', password_hash=hashed_pw)
            db.session.add(admin)
            db.session.commit()
            print("Database created & Admin user (admin/admin123) added!")
    sys.exit()

# --- PUBLIC ROUTES ---

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        # REGISTER GUEST
        name = request.form['name']
        email = request.form['email']
        # Generate a unique ticket ID
        unique_ticket = str(uuid.uuid4())[:8].upper()

        new_guest = Guest(name=name, email=email, ticket_id=unique_ticket, event_id=event.id)
        db.session.add(new_guest)
        db.session.commit()
        return redirect(url_for('ticket_view', ticket_id=unique_ticket))

    return render_template('event_detail.html', event=event)

@app.route('/ticket/<ticket_id>')
def ticket_view(ticket_id):
    guest = Guest.query.filter_by(ticket_id=ticket_id).first_or_404()
    event = Event.query.get(guest.event_id)

    # Generate QR Code in memory
    qr = qrcode.make(f"TICKET:{ticket_id} | EVENT:{event.title} | GUEST:{guest.name}")
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)

    # We pass the guest and event details to the template. 
    # The QR code would ideally be served via a separate route, 
    # but for simplicity, we will assume a placeholder or simple link in this guide.
    return render_template('ticket.html', guest=guest, event=event)

@app.route('/qr_image/<ticket_id>')
def qr_image(ticket_id):
    guest = Guest.query.filter_by(ticket_id=ticket_id).first_or_404()
    event = Event.query.get(guest.event_id)
    qr = qrcode.make(f"VALID TICKET\nID: {ticket_id}\nGuest: {guest.name}")
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

# --- ADMIN ROUTES ---

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and bcrypt.check_password_hash(admin.password_hash, password):
            login_user(admin)
            return redirect(url_for('dashboard'))
        flash('Login Failed', 'danger')
    return render_template('login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        category = request.form['category']
        description = request.form['description']
        new_event = Event(title=title, date=date, category=category, description=description)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('dashboard'))

    events = Event.query.all()
    # Data for Charts: Count guests per event
    event_titles = [e.title for e in events]
    guest_counts = [len(e.guests) for e in events]

    return render_template('dashboard.html', events=events, titles=event_titles, counts=guest_counts)

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)