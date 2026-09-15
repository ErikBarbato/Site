from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0007_playlist"),
    ]

    operations = [
        migrations.CreateModel(
            name="Perfil",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "foto",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="perfis/",
                    ),
                ),
                (
                    "usuario",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="perfil",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]