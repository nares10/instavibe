# Nexus 📱

A full-featured social media web application built with Django, featuring real-time notifications, user interactions, and a modern responsive design.

## 🌟 Features

- **User Authentication**
  - Email/password registration and login
  - Social authentication (Google, Facebook)
  - Secure password hashing

- **Profile Management**
  - User profile with bio and profile picture
  - Profile editing capabilities
  - Follow/Unfollow system
  - View followers and following lists

- **Post Management**
  - Create, edit, and delete posts
  - Image uploads with captions
  - View post details and interactions
  - Explore feed with posts from followed users

- **Social Interactions**
  - Like/Unlike posts
  - Comment on posts
  - Real-time notifications
  - WebSocket support for live updates

- **Messaging**
  - Direct messaging between users
  - Message persistence

- **Frontend**
  - Modern, responsive UI with Tailwind CSS
  - HTMX for dynamic interactions without page reloads
  - Mobile-friendly design

## 🛠️ Tech Stack

**Backend:**
- Django 5.2.5
- Django Channels (WebSockets)
- PostgreSQL
- Redis (for caching and WebSocket layer)
- Daphne (ASGI server)

**Frontend:**
- HTML/CSS with Tailwind CSS 4.1
- JavaScript with HTMX
- Bootstrap-like responsive design

**DevOps:**
- Docker & Docker Compose
- PostgreSQL 15 database

## 📋 Requirements

- Python 3.10+
- PostgreSQL 15+
- Redis
- Node.js (for Tailwind CSS compilation)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd nexus
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Node Dependencies (for Tailwind CSS)
```bash
npm install
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=nexus_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
REDIS_URL=redis://localhost:6379/0
```

### 6. Set Up Database
```bash
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Compile Tailwind CSS
```bash
python manage.py tailwind build
# For development with watch mode:
python manage.py tailwind start
```

### 9. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 🐳 Docker Setup

To run the application with Docker:

```bash
docker-compose up -d
```

This will start:
- Django application on port 8000
- PostgreSQL database on port 5432

Run migrations:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 📁 Project Structure

```
nexus/
├── nexus/                  # Main project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py             # URL routing
│   ├── asgi.py             # ASGI config for WebSockets
│   └── wsgi.py             # WSGI config for deployment
├── nexusapp/               # Main application
│   ├── models/             # Database models
│   │   ├── profile.py      # User profile model
│   │   ├── post.py         # Post model
│   │   ├── comment.py      # Comment model
│   │   ├── like.py         # Like model
│   │   ├── follow.py       # Follow relationship
│   │   ├── notification.py # Notifications
│   │   └── message.py      # Direct messages
│   ├── views.py            # View logic
│   ├── consumers.py        # WebSocket consumers
│   ├── forms.py            # Django forms
│   ├── urls.py             # App URL routing
│   ├── templates/          # HTML templates
│   │   └── nexusapp/
│   │       ├── base.html   # Base template
│   │       ├── feed.html   # Feed page
│   │       ├── profile.html # User profile
│   │       └── ...
│   └── static/             # Static files (CSS, JS)
├── mytheme/                # Tailwind theme configuration
├── requirements.txt        # Python dependencies
├── package.json            # Node dependencies
└── docker-compose.yml      # Docker configuration
```

## 💻 Available Commands

### Django Management
```bash
# Run development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create database migrations
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Access Django admin
# Navigate to http://localhost:8000/admin/
```

### Tailwind CSS
```bash
# Build Tailwind CSS
python manage.py tailwind build

# Watch for changes during development
python manage.py tailwind start
```

### Docker
```bash
# Build and start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web
```

## 🔑 Key Features Explained

### Real-Time Notifications
Uses Django Channels with WebSockets for real-time updates when users:
- Receive likes on their posts
- Receive comments on their posts
- Get followed/unfollowed

### Responsive Design
Built with Tailwind CSS for a mobile-first, responsive design that works on all screen sizes.

### HTMX Integration
Provides dynamic interactions without full page reloads:
- Like/unlike posts
- Add comments
- Follow/unfollow users

### Social Authentication
Supports login via Google and Facebook using django-allauth.

## 🗄️ Database Models

- **User Profile**: Extended Django User with bio and profile image
- **Post**: User-generated content with image and caption
- **Comment**: Text comments on posts
- **Like**: Track post and comment likes
- **Follow**: Track user relationships
- **Notification**: Real-time user notifications
- **Message**: Direct messaging between users

## 🔐 Security Features

- CSRF protection
- SQL injection prevention with Django ORM
- Password hashing
- Secure session management
- Cross-site scripting (XSS) protection

## 📝 API & Routes

### Authentication
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout

### User
- `/profile/<username>/` - View user profile
- `/profile/edit/` - Edit own profile
- `/<username>/followers/` - View followers
- `/<username>/following/` - View following

### Posts
- `/` - Home feed
- `/explore/` - Explore all posts
- `/post/<id>/` - View post details
- `/post/create/` - Create new post
- `/post/<id>/edit/` - Edit post
- `/post/<id>/delete/` - Delete post

### Interactions
- `/post/<id>/like/` - Like a post
- `/post/<id>/comment/` - Add comment
- `/follow/<username>/` - Follow user

### Messaging
- `/messages/` - Message inbox
- `/messages/<username>/` - Chat with user

## 🐛 Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_* environment variables
- Run `python manage.py migrate`

### WebSocket Not Working
- Ensure Redis is running
- Check Daphne ASGI server is active
- Verify ASGI_APPLICATION setting in settings.py

### Tailwind CSS Not Applied
- Run `python manage.py tailwind build`
- Clear browser cache
- Check static files are collected: `python manage.py collectstatic`

### Static Files Missing
```bash
python manage.py collectstatic --noinput
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Naresh Dewasi

## 📞 Support

For issues and questions, please open an issue in the repository.

---

**Happy coding! 🚀**
