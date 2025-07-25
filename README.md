 HEAD
# Farm Basket - Fresh Organic Produce Platform

Farm Basket is a comprehensive e-commerce platform that connects local farmers directly with consumers, enabling the sale and purchase of fresh, organic produce. Built with Django, PostgreSQL, and modern frontend technologies.

## 🌟 Features

### Customer Module
- **User Registration & Login**: Secure authentication system for customers
- **Product Browsing**: Browse and search through fresh organic products
- **Cart Management**: Add, remove, and update items in shopping cart
- **Order Placement & Tracking**: Place orders and track their status
- **Market Price Comparison**: Compare prices across different farmers

### Farmer Module
- **Vendor Registration & Login**: Specialized registration for farmers
- **Product Listing & Management**: Add, edit, and manage product listings
- **Order Management**: View and manage incoming orders
- **Sales Reports**: Comprehensive analytics and reporting
- **Market Price Viewing**: Access current market prices

### Admin Panel Module
- **Farmer Approval & Management**: Review and approve farmer applications
- **Product Monitoring**: Oversee product listings and quality
- **Order Oversight**: Monitor all orders and delivery status
- **Live Market Price Updates**: Manage market price information
- **User Management**: Comprehensive user administration

### Minor Modules
- **Authentication Module**: Secure role-based access control
- **Notification Module**: Real-time alerts and notifications
- **Feedback & Review Module**: Product ratings and reviews
- **Profile Management Module**: User profile customization
- **Search & Filter Module**: Advanced product discovery
- **Payment Module**: Secure payment processing (optional)
- **Live Market Price Integration**: Real-time market data (optional)

## 🛠️ Technology Stack

### Backend
- **Django 5.2.3**: Python web framework
- **PostgreSQL**: Primary database
- **Django Crispy Forms**: Form rendering and styling
- **Crispy Tailwind**: Tailwind CSS integration

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Styling with Tailwind CSS
- **JavaScript**: Interactive functionality
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Icon library

### Database
- **PostgreSQL**: Robust relational database
- **Django ORM**: Database abstraction layer

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd farm_basket
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
1. Create a PostgreSQL database:
```sql
CREATE DATABASE farm_basket_db;
CREATE USER farm_basket_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE farm_basket_db TO farm_basket_user;
```

2. Update database settings in `farm_basket_project/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'farm_basket_db',
        'USER': 'farm_basket_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
farm_basket/
├── accounts/                 # User authentication and profiles
├── products/                 # Product management
├── orders/                   # Order processing and cart
├── farmers/                  # Farmer-specific functionality
├── reviews/                  # Product reviews and ratings
├── notifications/            # Notification system
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── home.html            # Homepage
│   └── accounts/            # Account templates
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User-uploaded files
├── farm_basket_project/      # Django project settings
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/farm_basket_db
```

### Static Files
For production, collect static files:
```bash
python manage.py collectstatic
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📊 Database Models

### Core Models
- **User**: Custom user model with role-based access
- **CustomerProfile**: Customer-specific information
- **FarmerProfile**: Farmer-specific information and approval status
- **Product**: Product listings with pricing and stock
- **Category**: Product categorization
- **Order**: Order management and tracking
- **Cart**: Shopping cart functionality
- **Review**: Product reviews and ratings
- **Notification**: System notifications

## 🔐 Security Features

- Custom user authentication system
- Role-based access control (Customer, Farmer, Admin)
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure file uploads

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in settings
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure email settings
- [ ] Set up SSL/HTTPS
- [ ] Configure logging
- [ ] Set up backup system

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL add-on
- **DigitalOcean**: VPS with PostgreSQL
- **AWS**: EC2 with RDS
- **Google Cloud**: Compute Engine with Cloud SQL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0**: Initial release with core functionality
- Basic user authentication
- Product management
- Order processing
- Admin panel

## 📞 Contact

- **Project Link**: [https://github.com/yourusername/farm-basket](https://github.com/yourusername/farm-basket)
- **Email**: support@farmbasket.com

---

**Farm Basket** - Connecting farmers and consumers for fresh, organic produce! 🌱 
# Farm-Basket
Farm Basket – A Multi-Vendor Organic Marketplace for Direct Farmer-to-Consumer Sales
e666f528f504af91cb8e7ddb13d48c5e6b98863b
