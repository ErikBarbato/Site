from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
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
    visualizacoes = models.PositiveIntegerField(default=0, verbose_name="Visualizações")
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

    @property
    def average_rating(self):
        agg = self.avaliacoes.aggregate(avg=Avg('nota'))
        return agg.get('avg') or 0

    @property
    def comentarios_count(self):
        return self.comentarios.count()


class Comentario(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.CharField(max_length=200)
    cadastrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.texto}"

class Avaliacao(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
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


    


    