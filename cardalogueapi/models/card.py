from django.db import models

class Card(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=50)
    card_category = models.ForeignKey("Category", on_delete=models.DO_NOTHING)
    image = models.ImageField(
        upload_to='cardfrontimages', height_field=None,
        width_field=None, max_length=None, null=True)
    is_approved = models.BooleanField()
    set = models.ForeignKey("Set", on_delete=models.CASCADE)
    tag = models.ManyToManyField("Tag", through="CardTag", related_name="tags")
