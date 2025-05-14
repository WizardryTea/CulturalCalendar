# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from affiche.models import Theater, Performance

class Command(BaseCommand):
    help = 'Очищение данных из БД'

    def handle(self, *args, **options):
        # Clear existing data
        Performance.objects.all().delete()
        Theater.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Данные очищены!')) 