from django.db import models
from django.utils import timezone

from users.models import User


class Base(models.Model):
    created_at = models.DateTimeField(default=timezone.localtime)
    modified_at = models.DateTimeField(default=timezone.localtime)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.localtime()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Advertisement(Base):
    text = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, related_name='advertisements', on_delete=models.CASCADE, null=False)


class Comment(Base):
    text = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, null=False)
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE, name=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['advertisement', 'owner'], name='user_ad_uq')
        ]
