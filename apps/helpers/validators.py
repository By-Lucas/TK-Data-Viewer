import os

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from validate_docbr import CPF, CNPJ
from localflavor.br.validators import BRCPFValidator
from localflavor.br.forms import BRCNPJField, BRCPFField


def allow_only_pdf_validator(file):
    try:
        from PyPDF2 import PdfReader
        PdfReader(file)
    except Exception:
        raise ValidationError(_('Arquivo inválido. Só aceita PDF.'))


def allow_only_words_validator(value):
    validate = value.split(" ")
    preposition = ['da', 'dos', 'do', 'de', 'das', 'e']
    for prepo in preposition:
        if prepo in validate:
            validate.remove(prepo)

    if len(validate) < 2:
        raise ValidationError(_('Este campo deve conter mais de uma palavra'))


def allow_only_images_validator(value):
    'Em caso de erro, deixar somente o value em vez de value.name'
    ext = os.path.splitext(value.name)[1]  # cover-image.jpg
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Tipo de arquivo não suportado. extensões permitidas: ' + str(valid_extensions)))


def allow_only_arquives_validator(value):
    'Em caso de erro, deixar somente o value em vez de value.name'
    ext = os.path.splitext(value.name)[1]  # arquive.pdf
    valid_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Tipo de arquivo não suportado. extensões permitidas: ' + str(valid_extensions)))


def validator_cpf_or_cnpj(value):
    if not CPF().validate(value):
        if not CNPJ().validate(value):
            raise ValidationError(_('CNPJ ou CPF inválido!'))
