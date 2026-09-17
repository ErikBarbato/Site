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
    
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    foto = models.ImageField(upload_to="perfis/", null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

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

    def _get_youtube_id(self):
        from urllib.parse import parse_qs, urlparse

        if not self.link:
            return ""

        try:
            parsed = urlparse(self.link)
            hostname = (parsed.hostname or "").lower()

            if hostname in {"youtu.be", "www.youtu.be"}:
                return parsed.path.strip("/").split("/")[0]

            if hostname.endswith(("youtube.com", "youtube-nocookie.com")):
                video_id = parse_qs(parsed.query).get("v", [""])[0]
                if video_id:
                    return video_id

                parts = [part for part in parsed.path.split("/") if part]
                for marker in ("embed", "v", "shorts", "live"):
                    if marker in parts:
                        marker_index = parts.index(marker)
                        if marker_index + 1 < len(parts):
                            return parts[marker_index + 1]
        except (AttributeError, IndexError, TypeError, ValueError):
            return ""

        return ""

    @property
    def youtube_video_id(self):
        return self._get_youtube_id()

    @property
    def embed_url(self):
        video_id = self._get_youtube_id()
        if not video_id:
            return ""
        return f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    @property
    def converter_link(self):
        return self.embed_url

    @property
    def thumbnail_url(self):
        video_id = self._get_youtube_id()
        if not video_id:
            return "https://via.placeholder.com/480x360?text=Sem+Miniatura"
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

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


    
class HistoricoPesquisa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historicos')
    termo = models.CharField(max_length=255)
    data_pesquisa = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.termo}"


class HistoricoVideo(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="historicos_video",
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="historicos_visualizacao",
    )
    data_visualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "video"],
                name="unique_historico_video_usuario",
            )
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.video.titulo}"


class Playlist(models.Model):
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="playlists",
    )
    videos = models.ManyToManyField(Video, blank=True, related_name="playlists")

    def __str__(self):
        return f"{self.nome} - {self.usuario.username}"

    