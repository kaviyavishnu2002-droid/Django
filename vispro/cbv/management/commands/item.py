from django.core.management.base import BaseCommand
from cbv.models import Detail, Item, Book
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Add add_detail permission to user kavi'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        User.objects.create_user(
            username='kanakaraj',
            email='kanakarajvis@gmail.com',
            password='kanavis18.',
            is_staff=True
        )

        
        self.stdout.write(self.style.SUCCESS('Permission added successfully!'))
        