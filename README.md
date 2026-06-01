# Goat Pedigree Management System

A comprehensive web application for managing goat and sheep herd pedigree information, tracking ancestry, and generating insightful reports about your livestock.

## Features

### 📊 Dashboard & Reports

- **Statistics Overview**: View total animals, average age, gender distribution at a glance
- **Breed Distribution**: Separate breed analysis for goats and sheep with visual bar charts
- **Gender Distribution**: Interactive visualization of male/female ratio in your herd
- **Age Distribution**: Categorized age groups (0-1, 1-3, 3-5, 5+ years) with dynamic charts
- **Species Distribution**: Track goats vs sheep inventory

### 🌳 Family Tree

- Visual representation of goat and sheep ancestry
- Track parent-child relationships
- Identify lineage and bloodlines

### 📦 Inventory Management

- Complete herd inventory with detailed animal profiles
- Track breed, gender, species, birth date, and registration information
- Upload and manage animal photos
- Search and filter functionality

### 👥 User Management

- Secure authentication system
- User registration and login
- Admin panel for system management

### 📱 Responsive Design

- Mobile-friendly interface
- Works seamlessly on desktop, tablet, and mobile devices
- Tailwind CSS for modern, clean UI

## Tech Stack

### Backend

- **Django 5.1** - Web framework
- **Django REST Framework** - RESTful API
- **PostgreSQL** - Primary database (production)
- **SQLite** - Development database

### Frontend

- **React** - UI library (CDN-based)
- **Tailwind CSS** - Utility-first CSS framework
- **Bootstrap** - Additional styling components
- **Font Awesome** - Icon library

### Deployment

- **Python 3.11**
- **Virtual Environment** for dependency isolation

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL (for production)
- Git

### Local Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Goat-Pedigree.git
   cd Goat-Pedigree
   ```
2. **Create virtual environment**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**

   - Copy `.env.example` to `.env`
   - Update database credentials and SECRET_KEY
5. **Run migrations**

   ```bash
   python manage.py migrate
   ```
6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```
7. **Start development server**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://localhost:8000`

## Project Structure

```
Goat-Pedigree/
├── goat_project/          # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── goats/                 # Main Django app
│   ├── models.py          # Database models (Goat model)
│   ├── views.py           # View functions and API endpoints
│   ├── urls.py            # App-level URL routing
│   ├── serializers.py     # DRF serializers
│   ├── forms.py           # Django forms
│   └── templates/
│       └── goats/         # HTML templates
│           ├── home.html
│           ├── inventory.html
│           ├── tree.html
│           ├── reports.html
│           └── about.html
├── static/                # Static files (CSS, JS, images, icons)
├── media/                 # User-uploaded files (animal photos)
├── theme/                 # Tailwind configuration
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Database Models

### Goat Model

```python
- name: CharField - Animal's name
- breed: CharField - Breed type
- gender: CharField - Male or Female
- species: CharField - Goat or Sheep
- birth_date: DateField - Date of birth
- registration: CharField - Registration number
- description: TextField - Additional notes
- image: ImageField - Animal photo
- father: ForeignKey - Paternal parent
- mother: ForeignKey - Maternal parent
```

## API Endpoints

### Goat Management

- `GET /api/goats/` - List all animals
- `GET /api/goats/{id}/` - Get animal details
- `POST /api/goats/` - Create new animal
- `PUT /api/goats/{id}/` - Update animal
- `DELETE /api/goats/{id}/` - Delete animal

## Usage

### Viewing Reports

1. Navigate to the **Reports** page
2. View comprehensive statistics about your herd:
   - Total animals count
   - Average age of animals
   - Gender and breed distribution
   - Age group breakdown
   - Species distribution

### Managing Inventory

1. Go to **Inventory** page
2. Browse all animals in your herd
3. Click on an animal to view/edit details
4. Add new animals with the add button

### Viewing Family Tree

1. Access the **Tree** page
2. Explore ancestry relationships
3. Click on animals to navigate the tree

### Admin Panel

1. Login with superuser credentials
2. Visit `/admin` to access Django admin
3. Manage users, animals, and system settings

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_NAME=goatpedigreedb
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

## Deployment

### Production Settings

- Set `DEBUG = False` in `settings.py`
- Use PostgreSQL database
- Configure proper ALLOWED_HOSTS
- Set secure SECRET_KEY via environment variable
- Use HTTPS
- Configure proper CORS settings

### Deployment Platforms

The application can be deployed on:

- **Render** (recommended)
- **Heroku**
- **AWS** (EC2, RDS)
- **DigitalOcean**
- **Custom VPS**

See [deployment guide](./DEPLOYMENT.md) for detailed instructions.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email dossoukponganfleming@gmail.com or open an issue on GitHub.

## Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Advanced pedigree analysis
- [ ] Genetic testing integration
- [ ] Multi-farm management
- [ ] Export reports to PDF
- [ ] Data import/export functionality
- [ ] Dark mode theme
- [ ] Multi-language support

## Changelog

### Version 0.6.4

- Fixed Sheep Breeds Distribution display
- Updated Breed Distribution bars to green color for both species
- Improved responsive layout for reports page

### Version 0.6.0

- Separated Breed Distribution by species (Goat & Sheep)
- Enhanced reports dashboard with comprehensive statistics
- Added species tracking

See [CHANGELOG.md](CHANGELOG.md) for full version history.

---

**Made with ❤️ for goat and sheep farmers worldwide by Lucas DKP**
