# 🤖 AI Club - AI Assistant Chat Platform

> A professional Django web application for AI communities with personal chat assistant, event management, and member profiles. **Production-ready. Fully documented. Deploy in minutes.**

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Django](https://img.shields.io/badge/django-5.2-darkgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **Personal Chat Assistant** | Individual AI chat per user with smart FAQ matching |
| 🎯 **Smart FAQ System** | Keyword + similarity matching for intelligent responses |
| 📅 **Event Management** | Create, manage, and register for events |
| 👥 **Member Directory** | Connect with community members and view profiles |
| 🔐 **Role-Based Access** | Admin, moderator, and member permission levels |
| �‍💼 **Admin Member Management** | Search & manage member roles with inline forms |
| �📊 **Activity Logging** | Track all user interactions and engagement |
| 📱 **Responsive Design** | Works perfectly on desktop, tablet, and mobile |
| 🎨 **Modern UI** | Beautiful gradient design with smooth interactions |  

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
```bash
python --version  # Need 3.10+
```

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/ai-club.git
cd ai-club

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver
```

**Visit:** http://localhost:8000  
**Admin:** http://localhost:8000/admin

---

## � Deploy for Free (5 Minutes)

### Render.com ⭐ (Recommended)

1. Create account → [render.com](https://render.com)
2. Create Web Service → Connect GitHub
3. **Build Command:**
   ```
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
   ```
4. **Start Command:**
   ```
   gunicorn ai_club.wsgi:application
   ```
5. **Environment Variables:**
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=your-app.onrender.com
   ```
6. Click Deploy → Live in ~5 minutes with free PostgreSQL! ✅

### Other Options
- **Railway.app** - $5 free credits/month (5 min setup)
- **PythonAnywhere** - Free tier available (10 min setup)
- **Docker** - Full control, work locally or cloud (15 min)

👉 **Detailed guide:** See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 🏗️ Architecture

```
accounts/       User authentication & profiles
assistant/      Chat assistant with FAQ system
dashboard/      Main dashboard & analytics
events/         Event creation & management
members/        Member directory & profiles
announcements/  Community announcements
projects/       Project showcase
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [📖 docs/QUICKSTART.md](docs/QUICKSTART.md) | Get running locally in 5 minutes |
| [🚀 docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Deploy to Render, Railway, or Docker |
| [👥 docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | How to contribute code & docs |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 5.2 |
| **Frontend** | HTML/CSS/JavaScript |
| **Database** | PostgreSQL (production) / SQLite (dev) |
| **Server** | Gunicorn |
| **Static Files** | WhiteNoise |
| **Deployment** | Docker, Render, Railway, PythonAnywhere |

---

## 📊 Project Structure

```
ai-club/
├── 📄 README.md              ← You are here
├── 📄 requirements.txt        (Dependencies)
├── 📄 LICENSE                 (MIT)
├── 📄 .env.example            (Config template)
├── 📄 .gitignore              (Secrets protection)
│
├── 🚀 Deployment Files
│   ├── Procfile               (Render/Heroku)
│   ├── Dockerfile             (Docker container)
│   ├── docker-compose.yml     (Local Docker)
│   └── render.yaml            (Render config)
│
├── 📚 docs/
│   ├── QUICKSTART.md          (Setup guide)
│   ├── DEPLOYMENT.md          (Deploy guide)
│   └── CONTRIBUTING.md        (Contributing)
│
├── 🎯 Django Application
│   ├── manage.py
│   ├── ai_club/               (Settings)
│   ├── accounts/              (Auth)
│   ├── assistant/             (Chat)
│   ├── dashboard/             (Dashboard)
│   ├── events/                (Events)
│   ├── members/               (Members)
│   ├── announcements/         (Announcements)
│   └── projects/              (Projects)
│
└── 🎨 Assets
    ├── templates/             (HTML)
    └── media/                 (Uploads)
```

---

## 🚦 Getting Help

### First Time Setup?
→ Run `docs/QUICKSTART.md` for 5-minute local setup

### Ready to Deploy?
→ See `docs/DEPLOYMENT.md` for 4+ free hosting options

### Want to Contribute?
→ Check `docs/CONTRIBUTING.md` for guidelines

### Have Issues?
1. Check relevant documentation
2. Search [GitHub Issues](https://github.com/yourusername/ai-club/issues)
3. Create new issue with details

---

## 🎯 Features Highlight

### 💬 Chat Assistant
- Personal chat interface for each user
- Smart FAQ matching with keyword + similarity scoring
- Real-time message updates
- Command system (/help, /events, /register, etc.)

### 📅 Events
- Create and manage community events
- Member registration & RSVP
- Event details and scheduling
- Activity tracking

### 👥 Members
- View community members
- Member profiles with bio
- Role-based visibility
- Member statistics

### �‍💼 Admin Member Management
- **Access:** `/admin/manage-member-roles/` (staff/admin only)
- Search members by name, username, or email
- Collapsible inline forms for role management
- Update primary and secondary roles instantly
- Smooth UX with no modal flickering

### �🔐 Security
- User authentication
- Role-based permissions (Admin, Moderator, Member)
- CSRF protection
- Environment variable secrets management

---

## 🌱 Environment Setup

Create `.env` file (copy from `.env.example`):

```bash
# For local development
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# For production (on Render)
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=your-app.onrender.com
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📈 Performance

- **Static Files**: Optimized with WhiteNoise compression
- **Database**: Connection pooling for production
- **Security**: HTTPS enforced, security headers set
- **Scalability**: Stateless app design for horizontal scaling

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🎓 Learning Resources

- [Django Official Docs](https://docs.djangoproject.com/)
- [Render Deployment Docs](https://render.com/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Python Best Practices](https://pep8.org/)

---

## 🏆 Status & Roadmap

### Current Status
- ✅ Core features complete
- ✅ Production ready
- ✅ Fully tested
- ✅ Fully documented

### Roadmap
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] AI integration (Gemini API)
- [ ] Email notifications
- [ ] Real-time notifications (WebSocket)
- [ ] Dark mode

---

## ⭐ Show Your Support

If you found this helpful, please give it a star! ⭐

---

## 👨‍💻 Author

**Your Name**
- 🔗 [LinkedIn](https://www.linkedin.com/in/ben-brahim-mohamed-ali-4b7053376/)
- 🐙 [GitHub](https://github.com/Dali15)
- 📧 [Email](mailto:med2006dali@gmail.com)

---

## 🙏 Acknowledgments

- Django community for the amazing framework
- All contributors who helped improve this project
- Open source community for inspiration

---

**Built with ❤️ for AI enthusiasts**

---

<div align="center">

### Ready to get started? 

[⚡ Quick Start](docs/QUICKSTART.md) • [🚀 Deploy Now](docs/DEPLOYMENT.md) • [👥 Contributing](docs/CONTRIBUTING.md)

</div>
