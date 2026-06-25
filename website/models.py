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
        from urllib.parse import urlparse, parse_qs

        if not self.link:
            return ""

        # Se já for um link de embed, retorna o próprio link
        if "/embed/" in self.link:
            return self.link

        try:
            parsed = urlparse(self.link)
            netloc = parsed.netloc.lower()

            # youtu.be short link -> path component is the id
            if 'youtu.be' in netloc:
                video_id = parsed.path.lstrip('/')
                if video_id:
                    return f"https://www.youtube.com/embed/{video_id}"

            # youtube.com links
            if 'youtube' in netloc or 'youtube-nocookie' in netloc:
                # query param v
                qs = parse_qs(parsed.query)
                if 'v' in qs and qs['v']:
                    return f"https://www.youtube.com/embed/{qs['v'][0]}"

                # path may contain /embed/VIDEOID or /v/VIDEOID
                parts = parsed.path.split('/')
                for i, part in enumerate(parts):
                    if part in ('embed', 'v') and i + 1 < len(parts):
                        candidate = parts[i + 1]
                        return f"https://www.youtube.com/embed/{candidate}"

            # Fallback: return original link
            return self.link
        except Exception:
            return self.link

    @property
    def thumbnail_url(self):
        from urllib.parse import urlparse, parse_qs
        if not self.link:
            return ""

        try:
            parsed = urlparse(self.link)
            netloc = parsed.netloc.lower()

            video_id = None
            if 'youtu.be' in netloc:
                video_id = parsed.path.lstrip('/')
            elif 'youtube' in netloc or 'youtube-nocookie' in netloc:
                qs = parse_qs(parsed.query)
                if 'v' in qs and qs['v']:
                    video_id = qs['v'][0]
                else:
                    parts = parsed.path.split('/')
                    for i, part in enumerate(parts):
                        if part in ('embed', 'v') and i + 1 < len(parts):
                            video_id = parts[i + 1]
                            break

            if video_id:
                return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            return ""
        except Exception:
            return ""

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
    nota = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)]
    )
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


    


    