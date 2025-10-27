from django import forms
from django.db import models

from .validators import validate_cnpj, validate_cpf, validate_cpf_or_cnpj


class CPFField(models.CharField):
    default_validators = [validate_cpf]

    def __init__(self, verbose_name=None, *args, **kwargs):
        kwargs.setdefault("verbose_name", verbose_name)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = forms.TextInput(attrs={"data-inputmask": "'mask':'999.999.999-99'"})
        return super().formfield(**kwargs)


class CNPJField(models.CharField):
    default_validators = [validate_cnpj]

    def __init__(self, verbose_name=None, *args, **kwargs):
        kwargs.setdefault("verbose_name", verbose_name)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = forms.TextInput(attrs={"data-inputmask": "'mask':'99.999.999/9999-99'"})
        return super().formfield(**kwargs)


class CPForCNPJField(models.CharField):
    default_validators = [validate_cpf_or_cnpj]
