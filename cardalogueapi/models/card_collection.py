from django.db import models

class CardCollection(models.Model):
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
    collection = models.ForeignKey("Collection", on_delete=models.CASCADE)
