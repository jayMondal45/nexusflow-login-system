# NexusFlow Login System 🔐

A modern, secure, and beautiful authentication system built with Flask, featuring OTP-based password recovery and a stunning glassmorphic UI design.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## ✨ Features

### 🔒 Security Features
- **Secure User Authentication** - Email and password-based login system
- **OTP-Based Password Recovery** - 6-digit verification codes sent via email
- **Session Management** - Secure session handling with Flask sessions
- **Password Validation** - Strong password requirements enforcement
- **CSRF Protection** - Built-in form protection
- **Cache Control** - Prevents unauthorized access via browser back button

### 🎨 UI/UX Features
- **Modern Glassmorphic Design** - Beautiful frosted glass effect interface
- **Responsive Layout** - Works seamlessly on all devices
- **Smooth Animations** - Engaging micro-interactions and transitions
- **Toast Notifications** - Real-time feedback for user actions
- **Interactive Dashboard** - Stats cards, activity feed, and quick actions
- **Dropdown Menu** - User profile management interface

### 📧 Email Features
- **HTML Email Templates** - Professional styled emails
- **OTP Delivery** - Instant verification code delivery
- **Password Recovery** - Secure password retrieval system
- **Email Notifications** - Custom branded email communications

## 🚀 Demo

### Login Page
Clean and modern login interface with social authentication options (UI ready).

### Dashboard
Feature-rich dashboard with statistics, recent activity, and quick action cards.

### Password Recovery
Three-step recovery process: Request OTP → Verify Code → Receive Password

## 📋 Prerequisites

Before running this project, make sure you have:

- Python 3.8 or higher
- pip (Python package manager)
- A Gmail account for SMTP (or other email service)
- SQLite (comes with Python)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jayMondal45/nexusflow-login-system.git
cd nexusflow-login-system
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Email Settings

Open `main.py` and update the email configuration:

```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use App Password, not regular password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

**Important:** For Gmail, you need to:
1. Enable 2-Factor Authentication
2. Generate an App Password
3. Use the App Password in the code

[How to generate Gmail App Password](https://support.google.com/accounts/answer/185833)

### 5. Update Secret Key

Change the secret key in `main.py` for security:

```python
app.secret_key = "your_unique_secret_key_here"  # Generate a random string
```

## 🎯 Usage

### Run the Application

```bash
python main.py
```

The application will start at `http://127.0.0.1:5000/`

### Default Routes

- `/` - Login page
- `/register` - Registration page
- `/forgot-password` - Password recovery
- `/verify-otp` - OTP verification
- `/dashboard` - User dashboard (requires login)
- `/logout` - Logout

## 📁 Project Structure

```
nexusflow-login-system/
│
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── users.db               # SQLite database (auto-generated)
│
├── templates/
│   ├── login.html         # Login/Register page
│   ├── forgot_password.html   # Password recovery page
│   ├── verify_otp.html    # OTP verification page
│   └── index.html         # Dashboard page
│
└── static/
    ├── css/
    │   └── style.css      # Main stylesheet
    └── js/
        └── app.js         # JavaScript functionality
```

## 🗄️ Database Schema

### Users Table
| Column   | Type    | Description          |
|----------|---------|----------------------|
| id       | Integer | Primary key          |
| name     | String  | User's full name     |
| email    | String  | Unique email address |
| password | String  | User password        |

### PasswordReset Table
| Column     | Type     | Description              |
|------------|----------|--------------------------|
| id         | Integer  | Primary key              |
| email      | String   | User's email             |
| otp        | String   | 6-digit verification code|
| created_at | DateTime | OTP generation time      |
| used       | Boolean  | OTP usage status         |

## 🔐 Security Considerations

### Implemented Security Features
- ✅ Session-based authentication
- ✅ Password protection (plaintext - see improvements)
- ✅ OTP expiration (10 minutes)
- ✅ One-time OTP usage
- ✅ Cache control headers
- ✅ CSRF token support (Flask built-in)

### Recommended Improvements for Production

```python
# Install required packages
pip install bcrypt flask-limiter

# Implement password hashing
from bcrypt import hashpw, gensalt, checkpw

# Hash password during registration
hashed_password = hashpw(password.encode('utf-8'), gensalt())

# Verify password during login
if checkpw(password.encode('utf-8'), candidate.password):
    # Login successful
```

**Important Security Notes:**
1. **Never store passwords in plaintext** - Use bcrypt or Argon2
2. **Implement rate limiting** - Prevent brute force attacks
3. **Use environment variables** - For sensitive data
4. **Enable HTTPS** - In production deployment
5. **Regular security audits** - Keep dependencies updated

## 🎨 Customization

### Change Color Scheme

Edit `static/css/style.css`:

```css
/* Primary gradient colors */
background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);

/* Update to your brand colors */
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Update Branding

1. **Logo**: Replace SVG in templates
2. **App Name**: Change "NexusFlow" in all templates
3. **Email Templates**: Customize in `main.py`

## 🐛 Troubleshooting

### Common Issues

**1. Email not sending**
- Verify Gmail App Password is correct
- Check if "Less secure app access" is disabled (use App Password instead)
- Verify SMTP settings

**2. Database errors**
```bash
# Delete existing database and restart
rm users.db
python main.py
```

**3. Module not found errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**4. Session issues**
- Clear browser cookies
- Check if secret key is set
- Verify session configuration

## 📦 Dependencies

Create `requirements.txt`:

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
email-validator==2.0.0
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Deployment

### Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create new app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY="your_secret_key"
heroku config:set EMAIL_ADDRESS="your_email"
heroku config:set EMAIL_PASSWORD="your_app_password"

# Deploy
git push heroku main
```

### Deploy to Render/Railway

1. Connect your GitHub repository
2. Set environment variables in dashboard
3. Deploy automatically on push

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Jay Mondal**

- GitHub: [@jayMondal45](https://github.com/jayMondal45)
- Project Link: [https://github.com/jayMondal45/nexusflow-login-system](https://github.com/jayMondal45/nexusflow-login-system)

## 🙏 Acknowledgments

- Flask documentation and community
- Modern UI design inspiration
- Open source contributors

## 📸 Screenshots

### Login Page
Modern glassmorphic design with animated background effects.

### Registration
Clean registration form with real-time validation.

### Password Recovery
Three-step OTP-based recovery process.

### Dashboard
Feature-rich dashboard with statistics and quick actions.

---

### ⭐ Star this repository if you found it helpful!

### 🐛 Found a bug? [Create an issue](https://github.com/jayMondal45/nexusflow-login-system/issues)

---

**Made with ❤️ by Jay Mondal**
