from django.core.exceptions import ValidationError
from validate_docbr import CNPJ, CPF, PIS


def validate_cpf(number):
    cpf = CPF()
    if not cpf.validate(number):
        raise ValidationError("CPF inválido")


def validate_cnpj(number):
    cnpj = CNPJ()
    if not cnpj.validate(number):
        raise ValidationError("CNPJ inválido")


def validate_cpf_or_cnpj(number):
    cpf = CPF()
    cnpj = CNPJ()
    if not cpf.validate(number) and not cnpj.validate(number):
        raise ValidationError("CPF ou CNPJ inválido")


def validate_nis(number):
    nis = PIS()
    if not nis.validate(number):
        raise ValidationError("Nis inválido")
