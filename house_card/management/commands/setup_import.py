from django.core.management.base import BaseCommand
from house_card.models import Settlement
from django.utils import timezone

class Command(BaseCommand):
    help = 'Создает начальные данные для импорта'
    
    def handle(self, *args, **options):
        # Создаем населенный пункт по умолчанию
        settlement, created = Settlement.objects.get_or_create(
            administration_id=1,
            name="Основной населенный пункт",
            defaults={
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Населенный пункт по умолчанию создан')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Населенный пункт по умолчанию уже существует')
            )