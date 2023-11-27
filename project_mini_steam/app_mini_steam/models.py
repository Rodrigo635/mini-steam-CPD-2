from django.db import models

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    developer = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"ID: {self.id} - {self.name} by {self.developer}"
