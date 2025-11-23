from django.db.models import TextChoices


class StatusChoices(TextChoices):
    ISSUED = 'issued'
    EXPIRED = 'expired'
    RETURNED = 'returned'
