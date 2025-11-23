from django.core.management.base import BaseCommand
from books.tasks import create_fines


class Command(BaseCommand):
    help = 'Тестирование задачи обработки просроченных аренд'

    def handle(self, *args, **options):
        self.stdout.write("Запуск тестовой задачи...")
        create_fines()
        self.stdout.write(
            self.style.SUCCESS("Задача выполнена успешно")
        )