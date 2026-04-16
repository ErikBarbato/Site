from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tema(models.Model):
    nome = models.CharField(max_length=255)
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome}"

class Subtema(models.Model):
    nome = models.CharField(max_length=255)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='subtemas')
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome}"

class Video(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    link = models.URLField()
    ativo = models.BooleanField(default=True)
    subtema = models.ForeignKey(Subtema, on_delete=models.CASCADE, related_name='videos')
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo}"

class Comentario(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.CharField(max_length=200)
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.texto}"

class Avaliacao(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.PositiveSmallIntegerField()
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.nota}"

class Like(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField()
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.like}"


    


    