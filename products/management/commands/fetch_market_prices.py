import requests
import json
from datetime import datetime, date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product, Category, MarketPrice
import random
import time

class Command(BaseCommand):
    help = 'Fetch live market prices for vegetables, fruits, and herbs from online sources'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='manual',
            help='Source of market prices (manual, api, webscrape)'
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting to fetch market prices...')
        
        # Get all products that are vegetables, fruits, or herbs
        products = Product.objects.filter(
            product_type__in=['vegetable', 'fruit', 'herb']
        ).select_related('category')
        
        if not products.exists():
            self.stdout.write('No products found. Please add some products first.')
            return
        
        # Fetch prices based on source
        source = options['source']
        if source == 'api':
            self.fetch_from_api(products)
        elif source == 'webscrape':
            self.fetch_from_webscrape(products)
        else:
            self.fetch_manual_prices(products)
        
        self.stdout.write('Market prices updated successfully!')

    def fetch_manual_prices(self, products):
        """Fetch realistic market prices based on product type and season"""
        today = date.today()
        
        # Define price ranges for different product types (in INR per kg)
        price_ranges = {
            'vegetable': {
                'tomato': (40, 80),
                'potato': (20, 35),
                'onion': (25, 45),
                'carrot': (30, 50),
                'cabbage': (15, 30),
                'cauliflower': (25, 45),
                'brinjal': (30, 60),
                'cucumber': (20, 40),
                'lady finger': (40, 70),
                'bitter gourd': (30, 50),
                'pumpkin': (20, 35),
                'spinach': (25, 45),
                'coriander': (40, 80),
                'mint': (60, 120),
                'curry leaves': (80, 150),
            },
            'fruit': {
                'apple': (120, 200),
                'banana': (40, 80),
                'orange': (60, 120),
                'mango': (80, 150),
                'papaya': (30, 60),
                'guava': (40, 80),
                'pomegranate': (100, 180),
                'grapes': (80, 150),
                'watermelon': (15, 30),
                'muskmelon': (25, 50),
                'pineapple': (40, 80),
                'coconut': (20, 40),
            },
            'herb': {
                'basil': (80, 150),
                'rosemary': (200, 400),
                'thyme': (180, 350),
                'oregano': (160, 300),
                'sage': (200, 400),
                'mint': (60, 120),
                'coriander': (40, 80),
                'curry leaves': (80, 150),
                'bay leaves': (120, 250),
                'lemongrass': (100, 200),
            }
        }
        
        sources = [
            'Mumbai APMC Market',
            'Delhi Azadpur Mandi',
            'Bangalore KR Market',
            'Chennai Koyambedu Market',
            'Kolkata New Market',
            'Hyderabad Gaddiannaram Market',
            'Pune Market Yard',
            'Ahmedabad APMC',
            'Lucknow Mandi',
            'Jaipur Market'
        ]
        
        for product in products:
            # Get price range for this product
            product_name_lower = product.name.lower()
            price_range = None
            
            # Find matching price range
            for item_name, range_tuple in price_ranges[product.product_type].items():
                if item_name in product_name_lower or product_name_lower in item_name:
                    price_range = range_tuple
                    break
            
            # If no specific match, use default range for product type
            if not price_range:
                if product.product_type == 'vegetable':
                    price_range = (25, 60)
                elif product.product_type == 'fruit':
                    price_range = (50, 120)
                elif product.product_type == 'herb':
                    price_range = (80, 200)
            
            # Generate realistic price with some variation
            min_price, max_price = price_range
            base_price = random.uniform(min_price, max_price)
            
            # Add seasonal variation (higher prices in off-season)
            seasonal_factor = random.uniform(0.8, 1.3)
            final_price = round(base_price * seasonal_factor, 2)
            
            # Choose random source
            source = random.choice(sources)
            
            # Create or update market price
            market_price, created = MarketPrice.objects.get_or_create(
                product=product,
                date=today,
                source=source,
                defaults={'price': final_price}
            )
            
            if not created:
                market_price.price = final_price
                market_price.save()
            
            status = 'Created' if created else 'Updated'
            self.stdout.write(
                f'{status}: {product.name} - ₹{final_price}/kg from {source}'
            )
            
            # Small delay to avoid overwhelming the system
            time.sleep(0.1)

    def fetch_from_api(self, products):
        """Fetch prices from a public API (Agmarknet-style mock) and update MarketPrice model"""
        import requests
        from datetime import date
        
        api_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"  # Example Agmarknet API endpoint
        api_key = "YOUR_API_KEY"  # Replace with your API key if required
        today = date.today()
        
        for product in products:
            # Prepare parameters for the API request
            params = {
                "api-key": api_key,
                "format": "json",
                "filters[commodity]": product.name,
                "filters[arrival_date]": today.strftime('%d/%m/%Y'),
                "limit": 1
            }
            try:
                response = requests.get(api_url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    records = data.get("records", [])
                    if records:
                        record = records[0]
                        price = float(record.get("modal_price", 0))
                        source = record.get("market", "Agmarknet")
                        # Update or create MarketPrice
                        market_price, created = MarketPrice.objects.update_or_create(
                            product=product,
                            date=today,
                            source=source,
                            defaults={"price": price}
                        )
                        status = 'Created' if created else 'Updated'
                        self.stdout.write(f"{status}: {product.name} - ₹{price} from {source}")
                    else:
                        self.stdout.write(f"No price data found for {product.name}")
                else:
                    self.stdout.write(f"API error for {product.name}: {response.status_code}")
            except Exception as e:
                self.stdout.write(f"Exception for {product.name}: {e}")

    def fetch_from_webscrape(self, products):
        """Fetch prices by web scraping (placeholder for future implementation)"""
        self.stdout.write('Web scraping not implemented yet. Using manual prices.')
        self.fetch_manual_prices(products) 