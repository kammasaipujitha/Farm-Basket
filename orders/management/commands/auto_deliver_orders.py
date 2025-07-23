from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from orders.models import Order

class Command(BaseCommand):
    help = 'Automatically mark shipped vegetable/fruit orders as delivered after 24 hours'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        cutoff = now - timedelta(hours=24)
        # Find all shipped orders updated more than 24 hours ago
        orders = Order.objects.filter(
            status='shipped',
            updated_at__lte=cutoff,
            items__product__product_type__in=['vegetable', 'fruit']
        ).distinct()
        for order in orders:
            order.status = 'delivered'
            order.save()
            self.stdout.write(self.style.SUCCESS(
                f'Order {order.order_number} marked as delivered (auto-update)'
            )) 