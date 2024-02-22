from inventory.models import Product

class Command(BaseCommand):    
    help = 'Populates the expiry_date column with a default value for all existing rows with a null value'
    
    def handle(self, *args, **options):
        Product.objects.filter(expiry_date=None).update(expiry_date='2023-01-01')
        self.stdout.write(self.style.SUCCESS('Expiry date column populated with default value for all existing rows with a null value'))