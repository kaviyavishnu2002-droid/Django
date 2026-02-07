from django.core.management.base import BaseCommand
from cbv.models import Detail, Item, Book

class Command(BaseCommand):
    help = 'Add add_detail permission to user kavi'

    def handle(self, *args, **kwargs):
        Book.objects.create(author="Tom", pages=300, price=600)
        
        self.stdout.write(self.style.SUCCESS('Permission added successfully!'))
        

