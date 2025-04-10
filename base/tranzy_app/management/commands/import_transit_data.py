from django.core.management.base import BaseCommand
from base.tranzy_app.data_loader import load_transit_data
from django.conf import settings

class Command(BaseCommand):
    help = 'Import transit data from Tranzy API to Neo4j'

    def add_arguments(self, parser):
        parser.add_argument('--city', type=str, help='Specify a city to import data for')

    def handle(self, *args, **options):
        city = options.get('city')
        
        if city and city not in settings.TRANZY_AGENCY_MAPPING:
            self.stdout.write(self.style.ERROR(f'City "{city}" not supported. Available cities: {", ".join(settings.TRANZY_AGENCY_MAPPING.keys())}'))
            return
            
        self.stdout.write(f'Starting transit data import for {"all cities" if not city else city}...')
        success = load_transit_data(city)
        if success:
            self.stdout.write(self.style.SUCCESS('Successfully imported transit data'))
        else:
            self.stdout.write(self.style.ERROR('Failed to import transit data'))