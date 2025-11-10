from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class List(models.Model):
    owner = models.ForeignKey(
        User,
        related_name="lists",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    @property
    def name(self):
        return self.item_set.first().text

    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("id",)
        unique_together = ("list", "text")
