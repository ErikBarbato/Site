from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.test.utils import CaptureQueriesContext
from django.db import connection

from django.contrib.auth.models import User

from .models import Tema, Subtema, Video, Comentario


class VideoQueryOptimizationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="professor", password="senha123")
        self.client = Client()
        self.client.force_login(self.user)

        self.tema = Tema.objects.create(nome="Matemática", cadastrado_por=self.user)
        self.subtema = Subtema.objects.create(
            nome="Álgebra",
            tema=self.tema,
            cadastrado_por=self.user,
        )

        for index in range(5):
            video = Video.objects.create(
                titulo=f"Vídeo {index}",
                descricao="Descrição do vídeo",
                link="https://www.youtube.com/watch?v=abc123",
                subtema=self.subtema,
                cadastrado_por=self.user,
                cadastrado_em=timezone.now(),
            )
            Comentario.objects.create(
                video=video,
                texto=f"Comentário {index}",
                cadastrado_por=self.user,
            )

    def test_video_list_has_limited_queries(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("video_listar"))

        self.assertEqual(response.status_code, 200)
        self.assertLess(len(queries), 15)

    def test_video_detail_has_limited_queries(self):
        video = Video.objects.first()
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("video_detail", args=[video.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertLess(len(queries), 15)
