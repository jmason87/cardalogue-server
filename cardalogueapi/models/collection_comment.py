from django.db import models
from django.contrib.auth.models import User

class CollectionComment(models.Model):
    content = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey("Collection", on_delete=models.CASCADE)
