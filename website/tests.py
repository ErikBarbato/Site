from django.test import TestCase, Client
from django.test import override_settings
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.test.utils import CaptureQueriesContext
from django.db import connection

from django.contrib.auth.models import Group, User

from .models import Comentario, HistoricoVideo, Playlist, Subtema, Tema, Video


@override_settings(
    MIDDLEWARE=[
        middleware
        for middleware in settings.MIDDLEWARE
        if middleware != "debug_toolbar.middleware.DebugToolbarMiddleware"
    ]
)
class VideoQueryOptimizationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="professor", password="senha123")
        professor_group = Group.objects.create(name="Professor")
        self.user.groups.add(professor_group)
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


@override_settings(
    MIDDLEWARE=[
        middleware
        for middleware in settings.MIDDLEWARE
        if middleware != "debug_toolbar.middleware.DebugToolbarMiddleware"
    ]
)
class HistoricoVideoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="aluno",
            password="senha123",
        )
        self.outro_usuario = User.objects.create_user(
            username="outro_aluno",
            password="senha123",
        )
        self.client.force_login(self.user)

        tema = Tema.objects.create(nome="Matemática", cadastrado_por=self.user)
        subtema = Subtema.objects.create(
            nome="Álgebra",
            tema=tema,
            cadastrado_por=self.user,
        )
        self.video = Video.objects.create(
            titulo="Equações",
            descricao="Aula de equações",
            link="https://www.youtube.com/watch?v=abc123",
            subtema=subtema,
            cadastrado_por=self.user,
        )

    def test_acessar_video_cria_historico_para_usuario_logado(self):
        response = self.client.get(reverse("video_detail", args=[self.video.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            HistoricoVideo.objects.filter(
                usuario=self.user,
                video=self.video,
            ).exists()
        )

    def test_acessar_video_novamente_atualiza_registro_sem_duplicar(self):
        self.client.get(reverse("video_detail", args=[self.video.pk]))
        historico_anterior = HistoricoVideo.objects.get(
            usuario=self.user,
            video=self.video,
        )

        self.client.get(reverse("video_detail", args=[self.video.pk]))

        self.assertEqual(
            HistoricoVideo.objects.filter(
                usuario=self.user,
                video=self.video,
            ).count(),
            1,
        )
        self.assertEqual(
            HistoricoVideo.objects.get(pk=historico_anterior.pk).pk,
            historico_anterior.pk,
        )

    def test_historico_exibe_apenas_videos_do_usuario(self):
        outro_tema = Tema.objects.create(
            nome="História",
            cadastrado_por=self.outro_usuario,
        )
        outro_subtema = Subtema.objects.create(
            nome="Brasil",
            tema=outro_tema,
            cadastrado_por=self.outro_usuario,
        )
        outro_video = Video.objects.create(
            titulo="Outro vídeo",
            descricao="Outro conteúdo",
            link="https://www.youtube.com/watch?v=xyz789",
            subtema=outro_subtema,
            cadastrado_por=self.outro_usuario,
        )
        HistoricoVideo.objects.create(usuario=self.user, video=self.video)
        HistoricoVideo.objects.create(usuario=self.outro_usuario, video=outro_video)

        response = self.client.get(reverse("historico"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["historicos"]), [
            HistoricoVideo.objects.get(usuario=self.user, video=self.video),
        ])
        self.assertContains(response, "Equações")
        self.assertNotContains(response, "Outro vídeo")

    def test_criar_playlist_salva_para_usuario_logado_e_redireciona(self):
        response = self.client.post(
            reverse("criar_playlist"),
            {"nome": "Revisão de matemática"},
        )

        self.assertRedirects(response, reverse("historico"))
        self.assertTrue(
            Playlist.objects.filter(
                usuario=self.user,
                nome="Revisão de matemática",
            ).exists()
        )

    def test_criar_playlist_pelo_player_adiciona_video_atual(self):
        response = self.client.post(
            reverse("criar_playlist"),
            {
                "nome": "Aula atual",
                "video_id": self.video.pk,
                "next": reverse("video_detail", args=[self.video.pk]),
            },
        )

        self.assertRedirects(
            response,
            reverse("video_detail", args=[self.video.pk]),
        )
        playlist = Playlist.objects.get(usuario=self.user, nome="Aula atual")
        self.assertTrue(playlist.videos.filter(pk=self.video.pk).exists())

    def test_historico_carrega_apenas_playlists_do_usuario(self):
        Playlist.objects.create(usuario=self.user, nome="Minha playlist")
        Playlist.objects.create(
            usuario=self.outro_usuario,
            nome="Playlist de outro usuário",
        )

        response = self.client.get(reverse("historico"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.context["playlists"].values_list("nome", flat=True)),
            {"Assistir mais tarde", "Minha playlist"},
        )
        self.assertContains(response, "Minha playlist")
        self.assertNotContains(response, "Playlist de outro usuário")
        self.assertContains(response, "0 ")

    def test_usuario_pode_deletar_sua_playlist(self):
        playlist = Playlist.objects.create(
            usuario=self.user,
            nome="Excluir esta",
        )

        response = self.client.post(
            reverse("deletar_playlist", args=[playlist.pk]),
        )

        self.assertRedirects(response, reverse("historico"))
        self.assertFalse(Playlist.objects.filter(pk=playlist.pk).exists())

    def test_usuario_nao_pode_deletar_playlist_de_outro_usuario(self):
        playlist = Playlist.objects.create(
            usuario=self.outro_usuario,
            nome="Playlist protegida",
        )

        response = self.client.post(
            reverse("deletar_playlist", args=[playlist.pk]),
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Playlist.objects.filter(pk=playlist.pk).exists())

    def test_toggle_video_playlist_adiciona_e_remove_video(self):
        playlist = Playlist.objects.create(
            usuario=self.user,
            nome="Estudos",
        )

        response = self.client.post(
            reverse("toggle_video_playlist"),
            {
                "video_id": self.video.pk,
                "playlist_id": playlist.pk,
                "salvo": "true",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(playlist.videos.filter(pk=self.video.pk).exists())

        response = self.client.post(
            reverse("toggle_video_playlist"),
            {
                "video_id": self.video.pk,
                "playlist_id": playlist.pk,
                "salvo": "false",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(playlist.videos.filter(pk=self.video.pk).exists())

    def test_toggle_video_playlist_nao_permite_playlist_de_outro_usuario(self):
        playlist = Playlist.objects.create(
            usuario=self.outro_usuario,
            nome="Privada",
        )

        response = self.client.post(
            reverse("toggle_video_playlist"),
            {
                "video_id": self.video.pk,
                "playlist_id": playlist.pk,
                "salvo": "true",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(playlist.videos.filter(pk=self.video.pk).exists())

    def test_player_carrega_playlists_do_usuario_e_marca_video_salvo(self):
        playlist = Playlist.objects.create(usuario=self.user, nome="Estudos")
        playlist.videos.add(self.video)

        response = self.client.get(reverse("video_detail", args=[self.video.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertIn(playlist, response.context["playlists"])
        self.assertIn(playlist.pk, response.context["playlists_com_video"])

    def test_player_carrega_fila_da_playlist_do_usuario(self):
        playlist = Playlist.objects.create(usuario=self.user, nome="Sequência")
        playlist.videos.add(self.video)

        response = self.client.get(
            reverse("video_detail", args=[self.video.pk]),
            {"list": playlist.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["playlist_atual"], playlist)
        self.assertEqual(
            list(response.context["playlist_videos"]),
            [self.video],
        )
        self.assertContains(response, "Sequência")
        self.assertContains(response, "Todos")

    def test_historico_resumido_limita_oito_registros(self):
        for index in range(10):
            video = Video.objects.create(
                titulo=f"Vídeo {index}",
                descricao="Conteúdo",
                link=f"https://www.youtube.com/watch?v=abc{index:03d}",
                subtema=self.video.subtema,
                cadastrado_por=self.user,
            )
            registro = HistoricoVideo.objects.create(usuario=self.user, video=video)
            HistoricoVideo.objects.filter(pk=registro.pk).update(
                data_visualizacao=timezone.now() - timezone.timedelta(minutes=index)
            )

        response = self.client.get(reverse("historico"))

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.context["historicos"]), 8)

    def test_historico_completo_agrupa_por_data_e_isola_usuario(self):
        registro_hoje = HistoricoVideo.objects.create(
            usuario=self.user,
            video=self.video,
        )
        registro_ontem = HistoricoVideo.objects.create(
            usuario=self.user,
            video=Video.objects.create(
                titulo="Vídeo de ontem",
                descricao="Conteúdo",
                link="https://www.youtube.com/watch?v=yesterday",
                subtema=self.video.subtema,
                cadastrado_por=self.user,
            ),
        )
        hoje = timezone.localdate()
        HistoricoVideo.objects.filter(pk=registro_hoje.pk).update(
            data_visualizacao=timezone.now()
        )
        HistoricoVideo.objects.filter(pk=registro_ontem.pk).update(
            data_visualizacao=timezone.now() - timezone.timedelta(days=1)
        )
        outro_video = Video.objects.create(
            titulo="Vídeo de outro usuário",
            descricao="Conteúdo",
            link="https://www.youtube.com/watch?v=other",
            subtema=self.video.subtema,
            cadastrado_por=self.outro_usuario,
        )
        HistoricoVideo.objects.create(
            usuario=self.outro_usuario,
            video=outro_video,
        )

        response = self.client.get(reverse("historico_completo"))

        self.assertEqual(response.status_code, 200)
        grupos = response.context["grupos_historico"]
        self.assertEqual([grupo["titulo"] for grupo in grupos[:2]], ["Hoje", "Ontem"])
        self.assertContains(response, "Histórico completo")

