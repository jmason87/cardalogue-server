from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ManyToManyField("Card", through="CardCollection",
                                  related_name="cards_in_collection")
