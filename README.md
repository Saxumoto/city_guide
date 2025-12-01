# Davao City Guide

A comprehensive web application for discovering and sharing tourist attractions in Davao City, Philippines. Built with Django, this platform allows users to contribute attractions, rate and review them, and explore the city through an interactive map.

## Features

- 🗺️ **Interactive Map**: View all attractions on an interactive map powered by Leaflet
- 📍 **Attraction Management**: Create, edit, and delete attractions with detailed information
- ⭐ **Rating System**: Rate and review attractions with a 5-star system
- 🔍 **Search & Filter**: Search by name, description, or location, and filter by category
- 👤 **User Contributions**: Track your contributions and their approval status
- 🔐 **User Authentication**: Secure registration and login system
- ✅ **Admin Approval**: Attractions require admin approval before being visible to the public
- 📱 **Responsive Design**: Beautiful, modern UI that works on all devices

## Categories

- Nature & Outdoors
- Culture & History
- Food & Nightlife
- Shopping & Malls

## Technology Stack

- **Backend**: Django 5.0+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, Tailwind CSS (via CDN), JavaScript
- **Maps**: Leaflet.js
- **Image Handling**: Pillow
- **Deployment**: Compatible with Render, Heroku, and other Django hosting platforms

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd city_guide
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=
```

**Generate a secret key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### 8. Collect Static Files

```bash
python manage.py collectstatic
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
city_guide/
├── attractions/          # Main app
│   ├── models.py       # Database models (Attraction, Review)
│   ├── views.py        # View logic
│   ├── forms.py        # Form definitions
│   ├── urls.py         # URL routing
│   ├── admin.py        # Admin configuration
│   ├── templates/      # HTML templates
│   └── static/         # Static files (CSS, JS, images)
├── city_guide/         # Project settings
│   ├── settings.py     # Django settings
│   ├── urls.py         # Root URL configuration
│   └── wsgi.py         # WSGI configuration
├── media/              # User-uploaded files
├── staticfiles/        # Collected static files
├── db.sqlite3         # SQLite database (development)
├── manage.py          # Django management script
├── requirements.txt    # Python dependencies
└── .env               # Environment variables (not in git)
```

## Usage

### For Regular Users

1. **Register**: Create an account to contribute attractions
2. **Browse**: Explore attractions on the map and list view
3. **Search**: Use the search bar to find specific attractions
4. **Review**: Rate and review attractions you've visited
5. **Contribute**: Add new attractions (requires admin approval)

### For Administrators

1. **Login**: Access the admin panel at `/admin/`
2. **Approve**: Review and approve pending attractions
3. **Manage**: Edit or delete any attraction
4. **Monitor**: Track user contributions and reviews

## Deployment

### Render.com

1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Set start command: `gunicorn city_guide.wsgi:application`
5. Add environment variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-domain.onrender.com`
   - `DATABASE_URL` (auto-provided by Render PostgreSQL)

### Environment Variables for Production

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:port/database
SECURE_SSL_REDIRECT=True
```

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

After modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Admin Panel

1. Create superuser: `python manage.py createsuperuser`
2. Visit: `http://127.0.0.1:8000/admin/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Security

- Never commit `.env` file
- Use strong `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` properly
- Use HTTPS in production

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on the repository.

## Acknowledgments

- Davao City tourism community
- Django framework
- Leaflet.js for mapping
- Tailwind CSS for styling

---

**Built with ❤️ for Davao City**

