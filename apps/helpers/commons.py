from django.utils.translation import gettext_lazy as _

ADMINISTRATOR = 'adm_access'
COMMOM_USER = 'user_commom_access'
CLIPSE_AGENT = 'clipse_agent'
CLIPSE_SELLER = 'clipse_seller'
NATURAL_PERSON = 'NP'
LEGAL_PERSON = 'LP'

# SEXO
SEX_MALE = 'M'
SEX_FEMALE = 'F'

# ESTADO CIVIL
NOT_MARRIED = 'Solteiro'
MARRIED = 'Casado'
DIVORCED = 'Divorciado'
WIDOWER = 'Viuvo'
SEPARATE = 'Separado'

# TIPO DE EMPRESA
TYPE_CLINIC = 'C'
TYPE_CLIPSE_SELLER = 'CS'
TYPE_CLIPSE_AGENT = 'CA'

COMPANY_TYPE = (
    (TYPE_CLINIC, _('Cliníca')),
    (TYPE_CLIPSE_SELLER, _('Vendedor Clipse')),
    (TYPE_CLIPSE_AGENT, _('Agente Clipse')),
)

# STATUS DA CLINICA
ACTIVE_STATUS = 'A'
INACTIVE_STATUS = 'I'
BLOCKED_STATUS = 'B'

CLINICAL_STATUS = (
    (ACTIVE_STATUS, _('Ativa')),
    (INACTIVE_STATUS, _('Inativa')),
    (BLOCKED_STATUS, _('Bloqueada'))
)

# SEXO
SEX_CHOICES = (
    (SEX_MALE, _('Masculino')),
    (SEX_FEMALE, _('Feminino')),
)

# ESTADO CIVIL
CIVILLY_STATE = (
    (NOT_MARRIED, _('Solteiro')),
    (MARRIED, _('Casado')),
    (DIVORCED, _('Divorciado')),
    (WIDOWER, _('Viúvo')),
    (SEPARATE, _('Separado')),
)

BASE_ACCESS_LEVEL_CHOICES = (
    (ADMINISTRATOR, _('Administrador')),
    (COMMOM_USER, _('Usuário comum')),
)

ACCESS_LEVEL_CHOICES = (
    (ADMINISTRATOR, _('Administrador')),
    (COMMOM_USER, _('Usuário comum')),
)

USER_CLINIC_CHOICES = (
    (ADMINISTRATOR, _('Administrador')),
    (COMMOM_USER, _('Usuário comum')),
)

USER_ROLE_CHOICE = (
    (CLIPSE_AGENT, _('Agente Clipse')),
    (CLIPSE_SELLER, _('Vendedor Clipse')),
)

PERSON_TYPE_CHOICES = (
    (NATURAL_PERSON, _('Pessoa Física')),
    (LEGAL_PERSON, _('Pessoa Jurídica')),
)

# PERÍODO FATURAMENTO: MENSAL | QUIZENAL | SEMANAL
MONTHLY = 'M'
FORTNIGHTLY = 'Q'
WEEKLY = 'S'

BILLING_PERIOD_CHOICES = (
    (MONTHLY, _('Mensal')),
    (FORTNIGHTLY, _('Quinzenal')),
    (WEEKLY, _('Semanal')),
)

# TAXAS
RATE_YES = 'S'
RATE_NO = 'N'

RATE_CHOICES = (
    (RATE_YES, _('Sim')),
    (RATE_NO, _('Não')),
)

# DOCUMENTOS
DOCUMENTS_PJ_CHOICES = (
    ('social_contract', 'Contrato Social'),
    ('contract_amendment', 'Aditivo Contratual')
)

DOCUMENTS_PF_CHOICES = (
    ('rg', 'RG'),
    ('cpf', 'CPF'),
    ('cro', 'CRO'),
    ('cnh', 'CNH')
)

DOCUMENTS_CHOICES = DOCUMENTS_PJ_CHOICES + DOCUMENTS_PF_CHOICES
