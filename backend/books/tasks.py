import logging

from django.db.models import Q
from django.utils import timezone

from books.choices import StatusChoices
from books.consts import FINE_PER_DAY
from books.models import BookLoan, Fine

logger = logging.getLogger(__name__)


def create_fines():
    try:
        expired_loans = BookLoan.objects.filter(
            Q(return_date=timezone.now().date() - timezone.timedelta(days=1)) |
            Q(status=StatusChoices.EXPIRED.value)
        )

        if expired_loans.count() == 0:
            return

        loans_to_update_status = []
        all_fines_to_update_amount = []

        for loan in expired_loans:
            if loan.status != 'expired':
                loan.status = 'expired'
                loans_to_update_status.append(loan)

            fine = Fine.objects.get_or_create(
                loan_id=loan.id,
                defaults={"amount": 0},
            )[0]

            fine.amount += FINE_PER_DAY
            all_fines_to_update_amount.append(fine)

        if loans_to_update_status:
            BookLoan.objects.bulk_update(
                loans_to_update_status,
                ['status']
            )

        if all_fines_to_update_amount:
            Fine.objects.bulk_update(
                all_fines_to_update_amount,
                ['amount']
            )

    except Exception as e:
        logger.error(f"Error in fines create: {e}")