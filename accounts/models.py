from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from core.fields import CPFField
from core.utils import FormatStringFileUpload


class UserRole(models.TextChoices):
    SUPERADMIN = "Superadmin", "Superadmin"
    ADMIN = "Admin", "Administrador"
    COMMON = "Comum", "Comum"


class User(AbstractBaseUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_("Opcional. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas."),
    )

    full_name = models.CharField(_("Nome Completo"), max_length=100)
    email = models.EmailField(_("email address"), max_length=255, unique=True)
    cpf = CPFField(_("CPF"), max_length=14, unique=True)

    profile_photo = ProcessedImageField(
        verbose_name=_("Foto de Perfil do Usuário"),
        upload_to=FormatStringFileUpload("users/profile/{instance.id}/{filename}"),
        null=True,
        blank=True,
        processors=[ResizeToFit(width=350, upscale=False)],
        format="JPEG",
        options={"quality": 80},
    )

    role = models.CharField(
        max_length=30, choices=UserRole.choices, default=UserRole.COMMON, verbose_name=_("Perfil do Usuário")
    )

    # Configurações para autenticação por email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "cpf"]

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    @property
    def firstname(self):
        """Retorna o primeiro nome a partir do full_name"""
        if self.full_name:
            return self.full_name.split()[0]
        return ""

    @property
    def lastname(self):
        """Retorna o último nome a partir do full_name"""
        if self.full_name:
            parts = self.full_name.split()
            return parts[-1] if len(parts) > 1 else ""
        return ""

    def __str__(self) -> str:
        return self.email
