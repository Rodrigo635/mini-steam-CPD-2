from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    developer = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"ID: {self.id} - {self.name} by {self.developer}"

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"ID: {self.id} - {self.titulo}"

    def save(self, *args, **kwargs):
        if not self.usuario_id:
            self.usuario = User.objects.first()

        super().save(*args, **kwargs)

class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    imagem = models.ImageField(upload_to='noticias/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} - {self.titulo}"