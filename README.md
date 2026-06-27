# Django Blog

A full-featured blog built with Django 6, PostgreSQL/MySQL, and Docker. Features comprehensive test coverage (97%).

## Tech Stack

- **Backend**: Django 6.0.4, Python 3.12
- **Database**: PostgreSQL (default) or MySQL
- **Frontend**: Django Templates, HTML5, CSS3
- **Editor**: django-summernote (WYSIWYG)
- **Deploy**: Docker, Gunicorn
- **Testing**: pytest, pytest-django, pytest-cov (97% coverage)

## Project Structure

```
├── djangoapp/                 # Django application code
│   ├── blog/                  # Main app (posts, pages, tags)
│   ├── site_setup/            # Site configuration
│   ├── project/               # Project settings
│   ├── utils/                 # Utilities (images, validators)
│   ├── tests.py               # App tests
│   └── requirements.txt       # Dependencies
├── data/                      # Persistent data (Docker volumes)
├── scripts/
│   └── commands.sh            # Container entrypoint
├── docker-compose files       # PostgreSQL or MySQL configs
└── README.md                  # This file
```

## Local Development

### Prerequisites

- Docker and Docker Compose
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd blog
   ```

2. **Configure environment**
   ```bash
   # Copy and edit the .env file
   cp djangoapp/.env.example djangoapp/.env
   # Edit djangoapp/.env with your settings
   ```

3. **Start with PostgreSQL** (recommended - 3x smaller image)
   ```bash
   docker compose -f psql_docker-compose.yml up -d --build
   ```

   **Or with MySQL:**
   ```bash
   docker compose -f mysql_docker-compose.yml up -d --build
   ```

4. **Access the blog**
   - Blog: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Default user: create via `docker exec`

## Testing

The project includes **44 tests** with **97% code coverage**.

### Run all tests

```bash
cd djangoapp
python -m pytest
```

### Run tests for a specific app

```bash
python -m pytest blog/tests.py
python -m pytest site_setup/tests.py
python -m pytest utils/tests.py
```

### Coverage report

```bash
python -m pytest --cov=. --cov-report=html
# Open htmlcov/index.html in your browser
```

### Available Tests

- **Models**: Tag, Category, Page, Post, PostAttachment, SiteSetup, MenuLink
- **Views**: index, post detail, page detail, category, tag, search, created_by
- **Admin**: PostAdmin (link, save_model), SiteSetupAdmin (has_add_permission)
- **Utils**: resize_image, validate_png

## Switching Between PostgreSQL and MySQL

1. **requirements.txt**: Uncomment the driver for your chosen database
2. **Dockerfile**: Adjust FROM if needed (Alpine base vs Slim)
3. **settings.py**: Configure the DATABASES block
4. **.env**: Set POSTGRES_* or MYSQL_* variables
5. **Network**: Use `172.17.0.1` as host (not `localhost`)

> **Note**: PostgreSQL uses ~191MB vs MySQL ~835MB (Docker image 3.3x smaller).

## Features

- Posts with WYSIWYG editor (Summernote)
- Categories and Tags
- Static pages
- Post search
- Pagination
- Image upload with automatic resizing
- SEO-friendly URLs (auto-generated slugs)
- Custom admin interface
- Dynamic site settings

## Useful Commands

```bash
# View logs
docker logs djangoapp_psql -f

# Django shell
docker exec -it djangoapp_psql python manage.py shell

# Create superuser
docker exec -it djangoapp_psql python manage.py createsuperuser

# Run migrations
docker exec -it djangoapp_psql python manage.py migrate

# Collect static files
docker exec -it djangoapp_psql python manage.py collectstatic
```

## License

This project is open source. Feel free to use and modify.

---

**Built with Django 6**
