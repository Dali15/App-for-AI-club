# Quick Start Guide - 5 Minutes

## Installation & Local Setup

### 1. Prerequisites
```bash
# Verify Python 3.10+
python --version

# Verify pip installed
pip --version
```

### 2. Clone & Setup (3 minutes)
```bash
# Clone repository
git clone https://github.com/yourusername/ai-club.git
cd ai-club

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure (1 minute)
```bash
# Copy environment file
cp .env.example .env

# Edit .env - change these only:
# DEBUG=True (for local development)
# SECRET_KEY=your-key (optional, has default)
```

### 4. Database Setup (1 minute)
```bash
python manage.py migrate
python manage.py createsuperuser  # Create admin account
```

### 5. Run
```bash
python manage.py runserver
```

**Visit:** http://localhost:8000
**Admin:** http://localhost:8000/admin

---

## Deploy to Render (5 minutes)

1. **Push to GitHub** (if not already)
   ```bash
   git push origin main
   ```

2. **Create Render Account** → [render.com](https://render.com)

3. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect GitHub repo
   - Fill in details:
     - **Name:** ai-club
     - **Runtime:** Python 3.11
     - **Build:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
     - **Start:** `gunicorn ai_club.wsgi:application`

4. **Environment Variables**
   ```
   DEBUG=False
   SECRET_KEY=<generate-new>
   ALLOWED_HOSTS=<your-app>.onrender.com
   ```

5. **Deploy** → Click "Create Web Service"

**Done!** Your app is live in ~5 minutes ✅

---

## Common Issues & Fixes

### Port Already in Use
```bash
python manage.py runserver 8080
```

### Database Errors
```bash
python manage.py migrate --fake-initial
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Permission Issues (macOS/Linux)
```bash
chmod +x manage.py
```

---

## File Structure

```
ai-club/
├── manage.py              ← Run: python manage.py ...
├── requirements.txt       ← Dependencies
├── .env.example          ← Copy to .env
├── Procfile              ← For Heroku/Render
├── docker-compose.yml    ← For Docker
├── README.md             ← Full documentation
├── ai_club/              ← Settings folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/             ← User management
├── assistant/            ← Chat assistant
├── dashboard/            ← Main dashboard
├── events/               ← Events management
└── templates/            ← HTML files
```

---

## Next Steps

1. **Explore Admin Panel**
   - http://localhost:8000/admin
   - Add FAQ entries, events, announcements

2. **Customize**
   - Edit `templates/base.html` for branding
   - Modify colors in template stylesheets
   - Add your own features

3. **Deploy**
   - Follow deployment guide
   - Use free hosting (Render, Railway)
   - Add to GitHub

4. **Share**
   - Post on LinkedIn
   - Share on GitHub
   - Contribute to open source

---

## Key Commands Cheat Sheet

```bash
# Server
python manage.py runserver

# Database
python manage.py migrate           # Apply migrations
python manage.py makemigrations    # Create migrations
python manage.py createsuperuser   # Create admin

# Static Files
python manage.py collectstatic

# Shell (interactive)
python manage.py shell

# Tests
python manage.py test

# Help
python manage.py help
```

---

## Useful Links

- **Django Docs:** https://docs.djangoproject.com/
- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app/
- **Python Docs:** https://docs.python.org/

---

## Support

Issues? Check:
1. README_DEPLOYMENT.md
2. GitHub Issues
3. Django Documentation
4. Render/Railway Support

---

**Version:** 1.0  
**Last Updated:** January 2026  
**Status:** ✅ Production Ready
