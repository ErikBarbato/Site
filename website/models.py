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
    
    @property
    def converter_link(self):
        import re
        if not self.link:
            return ""

        # Se já for um link de embed, retorna o próprio link
        if "/embed/" in self.link:
            return self.link

        # Regex para extrair o ID do vídeo de diversos formatos (youtube.com, youtu.be, etc)
        regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        
        match = re.search(regex, self.link)
        
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
        
        # Caso não seja um link válido do YouTube, retorna o link original ou string vazia
        return self.link


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


    


    