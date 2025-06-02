from django.db import models
from django.contrib.auth import get_user_model
from project.models import Project
from django.utils import timezone

User = get_user_model()

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.project.is_cancelled or timezone.now() > self.project.end_time:
            raise ValueError("You cannot donate to a cancelled or expired project.")
        super().save(*args, **kwargs)



