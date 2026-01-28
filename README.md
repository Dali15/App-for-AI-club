# 🎉 AI CLUB - Production Ready

A professional Django application for AI communities with personal chat assistant, event management, and member profiles.

## ⚡ Quick Start

### 🏃 Run Locally (5 minutes)
\\\ash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
\\\
→ [See QUICKSTART.md](QUICKSTART.md) for details

### 🚀 Deploy for Free
→ [See README_DEPLOYMENT.md](README_DEPLOYMENT.md)
- Render.com (⭐ 5 min, includes PostgreSQL)
- Railway.app (5 min, \ free credits)
- PythonAnywhere (10 min, beginner-friendly)
- Docker (15 min, full control)

---

## ✨ Features

- **Personal Chat Assistant** - Individual AI-powered chat per user
- **Smart FAQ Matching** - Intelligent keyword + similarity matching
- **Event Management** - Create, manage, and register for events
- **Member Directory** - Connect with community members
- **Role-Based Permissions** - Admin, moderator, and member roles
- **Activity Logging** - Track all user interactions
- **Responsive Design** - Works on desktop and mobile

---

## 🏗️ Architecture

\\\
accounts/       # User authentication & profiles
assistant/      # Chat assistant & FAQ system
dashboard/      # Main dashboard & analytics
events/         # Event management
members/        # Member directory
announcements/  # Community announcements
projects/       # Project showcase
\\\

---

## 🔐 Security

✅ No hardcoded secrets  
✅ Environment variables for all credentials  
✅ Production security headers  
✅ HTTPS/SSL ready  
✅ CSRF & XSS protection  

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup |
| [README_DEPLOYMENT.md](README_DEPLOYMENT.md) | Deployment guide |
| [docs/](docs/) | Complete documentation |

---

## 💻 Tech Stack

- **Backend:** Django 5.2
- **Database:** PostgreSQL (production) / SQLite (dev)
- **Server:** Gunicorn + WhiteNoise
- **Frontend:** Bootstrap 5

---

## 🚀 Deploy Now

\\\ash
# Push to GitHub
git push origin main

# Deploy to Render (recommended)
# See README_DEPLOYMENT.md for step-by-step
\\\

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**Status:** ✅ Production Ready | **Version:** 1.0 | **Updated:** Jan 2026
