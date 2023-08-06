from django.db import models
from django.utils import timezone


class ExecutionLog(models.Model):
    STATUS_CHOICES = (
        ("success", "Success"),
        ("failure", "Failure"),
    )

    name = models.CharField(max_length=255)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
    )
    note = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "scripts_execution_log"
        ordering = ["-start_time"]

    def update_execution_log(self, status, note=None, error_message=None):
        self.status = status
        self.note = note
        self.error_message = error_message
        self.end_time = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.name}"
