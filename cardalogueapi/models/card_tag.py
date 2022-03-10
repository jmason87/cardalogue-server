from django.db import models

class CardTag(models.Model):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
