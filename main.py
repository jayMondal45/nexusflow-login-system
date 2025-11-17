from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from functools import wraps

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "your_secret_key_here"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# Email configuration
EMAIL_ADDRESS = "your_gamil@gmail.com"
EMAIL_PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_otp_email(email, otp):
    """Send OTP to user's email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Password Reset OTP"
        
        body = f'''
        <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>You have requested to reset your password. Please use the following OTP to verify your identity:</p>
                <h1 style="background: #f0f0f0; padding: 10px; text-align: center; border-radius: 5px; letter-spacing: 5px;">{otp}</h1>
                <p>This OTP will expire in 10 minutes.</p>
                <p>If you didn't request this, please ignore this email.</p>
                <br>
                <p>Best regards,<br>NexusFlow Team</p>
            </body>
        </html>
        '''
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit() 
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_password_email(email, password):
    """Send password to user's email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Your Password"
        
        body = f'''
        <html>
            <body>
                <h2>Your Account Password</h2>
                <p>As requested, here is your account password:</p>
                <h1 style="background: #f0f0f0; padding: 10px; text-align: center; border-radius: 5px;">{password}</h1>
                <p>For security reasons, we recommend changing your password after logging in.</p>
                <p>If you didn't request this, please contact our support team immediately.</p>
                <br>
                <p>Best regards,<br>NexusFlow  Team</p>
            </body>
        </html>
        '''
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def no_cache(f):
    """Decorator to prevent caching of pages"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return decorated_function

@app.route("/", methods=["GET", "POST"])
@no_cache
def login():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        action = request.form.get("action")

        if action == "login":
            candidate = User.query.filter_by(email=email).first()

            if candidate:
                if candidate.password == password:
                    session['user_id'] = candidate.id
                    session['user_name'] = candidate.name
                    session['user_email'] = candidate.email
                    flash("Login successful!", "success")
                    return redirect(url_for('dashboard'))
                else:
                    flash("Invalid password!", "error")
            else:
                flash("Email not found.", "error")

        elif action == "forgot_password":
            return redirect(url_for('forgot_password'))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
@no_cache
def register():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash("Passwords do not match. Please try again!", "error")
            return redirect(url_for('register'))
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("This email already exists. Try with different one.", "error")
            return redirect(url_for("register"))
        
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("User created successfully!", "success")
        return redirect(url_for("login"))

    return render_template("login.html", active_tab="register")

@app.route("/forgot-password", methods=["GET", "POST"])
@no_cache
def forgot_password():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == "POST":
        email = request.form.get("email")
        action = request.form.get("action")
        
        if action == "send_otp":
            user = User.query.filter_by(email=email).first()
            
            if user:
                # Generate 6-digit OTP
                otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                
                # Store OTP in database
                reset_request = PasswordReset(email=email, otp=otp)
                db.session.add(reset_request)
                db.session.commit()
                
                # Send OTP via email
                if send_otp_email(email, otp):
                    session['reset_email'] = email
                    flash("OTP sent to your email", "success")
                    return redirect(url_for('verify_otp'))
                else:
                    flash("Failed to send OTP. Please try again.", "error")
            else:
                flash("Email not found in our system", "error")
    
    return render_template("forgot_password.html")

@app.route("/verify-otp", methods=["GET", "POST"])
@no_cache
def verify_otp():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if 'reset_email' not in session:
        flash("Please request a password reset first", "error")
        return redirect(url_for('forgot_password'))
    
    if request.method == "POST":
        otp = request.form.get("otp")
        email = session['reset_email']
        
        # Find valid OTP (not used and within 10 minutes)
        valid_time = datetime.utcnow().timestamp() - 600  # 10 minutes ago
        reset_request = PasswordReset.query.filter(
            PasswordReset.email == email,
            PasswordReset.otp == otp,
            PasswordReset.used == False,
            PasswordReset.created_at >= datetime.fromtimestamp(valid_time)
        ).first()
        
        if reset_request:
            # Mark OTP as used
            reset_request.used = True
            db.session.commit()
            
            # Get user and send password
            user = User.query.filter_by(email=email).first()
            if user and send_password_email(email, user.password):
                session.pop('reset_email', None)
                flash("Password sent to your email", "success")
                return redirect(url_for('login'))
            else:
                flash("Failed to send password. Please try again.", "error")
        else:
            flash("Invalid or expired OTP. Please try again.", "error")
    
    return render_template("verify_otp.html")

@app.route("/dashboard")
@login_required
@no_cache
def dashboard():
    return render_template("index.html", 
                         name=session.get('user_name'),
                         email=session.get('user_email'))

@app.route("/logout")
@no_cache
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)