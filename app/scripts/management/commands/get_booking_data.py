from django.core.management.base import BaseCommand
from django.utils import timezone
from scripts.models import ExecutionLog
from scripts.utils import BookingData


class Command(BaseCommand):
    help = 'Get the latest successful entry with name "get_booking_data"'

    def handle(self, *args, **options):
        last_run = (
            ExecutionLog.objects.filter(
                name="get_booking_data",
                status="success",
            )
            .order_by("-start_time")
            .first()
        )

        booking_data = BookingData("DU")

        if last_run:
            booking_data.set_params(last_run, timezone.now())
        else:
            booking_data.set_params(timezone.now().replace(hour=0, minute=0, second=0), timezone.now())

        execution_log = ExecutionLog(name="get_booking_data")
        execution_log.save()

        execution_log.update_execution_log("success", f"{booking_data.destination} Reports")
