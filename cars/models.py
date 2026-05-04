# cars/models.py

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet


class Car(models.Model):
    STATUS_CHOICES = [
        ('estoque', 'Estoque'),
        ('vendido', 'Vendido'),
        ('reservado', 'Reservado'),
    ]

    MAINTENANCE_CHOICES = [
        ('nao_precisa', 'Não Precisa'),
        ('nao_tem', 'Não Tem'),
        ('precisa', 'Precisa'),
    ]

    # Aba FIPE
    fipe_code = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='Código FIPE'
    )

    fipe_initial_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Preço Inicial FIPE'
    )

    fipe_current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Preço Atual FIPE'
    )

    brand = models.CharField(
        max_length=100,
        default='Marca não informada',
        verbose_name='Marca'
    )

    model = models.CharField(
        max_length=100,
        default='Modelo não informado',
        verbose_name='Modelo'
    )

    year = models.IntegerField(
        default=0,
        verbose_name='Ano'
    )

    plate = models.CharField(
        max_length=20,
        default='SEM-PLACA',
        verbose_name='Placa'
    )

    color = models.CharField(
        max_length=50,
        default='Branco',
        verbose_name='Cor'
    )

    mileage = models.IntegerField(
        default=0,
        verbose_name='Quilometragem'
    )

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Preço de Compra'
    )

    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Preço de Venda'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='estoque',
        verbose_name='Status'
    )

    publication_sites = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Sites de Publicação'
    )

    image = models.ImageField(
        upload_to='cars/',
        blank=True,
        null=True,
        verbose_name='Imagem'
    )

    # Aba Manutenção
    needs_cleaning = models.CharField(
        max_length=20,
        choices=MAINTENANCE_CHOICES,
        default='nao_precisa',
        verbose_name='Precisa Limpar?'
    )

    needs_sanitizing = models.CharField(
        max_length=20,
        choices=MAINTENANCE_CHOICES,
        default='nao_precisa',
        verbose_name='Precisa Higienizar?'
    )

    has_spare_key = models.CharField(
        max_length=20,
        choices=MAINTENANCE_CHOICES,
        default='nao_precisa',
        verbose_name='Tem Chave Reserva?'
    )

    has_cautelar = models.CharField(
        max_length=20,
        choices=MAINTENANCE_CHOICES,
        default='nao_precisa',
        verbose_name='Tem Cautelar?'
    )

    has_procuracao = models.CharField(
        max_length=20,
        choices=MAINTENANCE_CHOICES,
        default='nao_precisa',
        verbose_name='Tem Procuração?'
    )

    has_crlv = models.CharField(
        max_length=20,
        choices=MAINTENANCE_CHOICES,
        default='nao_precisa',
        verbose_name='Tem CRLV?'
    )

    # Aba Anúncios
    ad_olx = models.BooleanField(default=False, verbose_name='OLX')
    ad_webmotors = models.BooleanField(default=False, verbose_name='WebMotors')
    ad_icarros = models.BooleanField(default=False, verbose_name='iCarros')
    ad_mercado_livre = models.BooleanField(default=False, verbose_name='Mercado Livre')
    ad_facebook = models.BooleanField(default=False, verbose_name='Facebook')
    ad_instagram = models.BooleanField(default=False, verbose_name='Instagram')

    other_ad_sites = models.CharField(
    max_length=255,
    blank=True,
    default='',
    verbose_name='Outros Sites')

    # Aba Observações
    observations = models.TextField(
        blank=True,
        default='',
        verbose_name='Observações'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.brand} {self.model} - {self.year}'

    @property
    def name(self):
        return f'{self.brand} {self.model}'

    @property
    def price(self):
        return self.sale_price


class Sale(models.Model):
    BUYER_TYPE_CHOICES = [
        ('fisica', 'Pessoa Física'),
        ('juridica', 'Pessoa Jurídica'),
    ]

    car = models.ForeignKey(
        Car,
        on_delete=models.PROTECT,
        related_name='sales',
        verbose_name='Carro'
    )

    sale_date = models.DateField(
        default=timezone.now,
        verbose_name='Data da Venda'
    )

    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Valor da Venda'
    )

    payment_method = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Forma de Pagamento'
    )

    buyer_type = models.CharField(
        max_length=20,
        choices=BUYER_TYPE_CHOICES,
        default='fisica',
        verbose_name='Tipo de Comprador'
    )

    buyer_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Nome Completo'
    )

    cpf = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name='CPF'
    )

    rg = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name='RG'
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Endereço'
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        default='',
        verbose_name='Telefone'
    )

    email = models.EmailField(
        blank=True,
        default='',
        verbose_name='E-mail'
    )

    observations = models.TextField(
        blank=True,
        default='',
        verbose_name='Observações'
    )

    profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Lucro'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.profit = self.sale_price - self.car.purchase_price

        self.car.status = 'vendido'
        self.car.save(update_fields=['status'])

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Venda - {self.car}'
class VehicleDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('crlv', 'CRLV'),
        ('nota_fiscal', 'Nota Fiscal'),
        ('recibo', 'Recibo'),
        ('contrato', 'Contrato'),
        ('laudo', 'Laudo'),
        ('seguro', 'Seguro'),
        ('outro', 'Outro'),
    ]

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Carro'
    )

    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name='Tipo de Documento'
    )

    name = models.CharField(
        max_length=120,
        verbose_name='Nome do Documento'
    )

    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='Observações'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.car}'


class VehicleDocumentImage(models.Model):
    document = models.ForeignKey(
        VehicleDocument,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='documents/',
        verbose_name='Imagem'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Imagem de {self.document.name}'

def get_credentials_fernet():
    return Fernet(settings.CREDENTIALS_ENCRYPTION_KEY.encode())


class AppConfiguration(models.Model):
    access_password_hash = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Senha de Proteção'
    )

    itau_email_encrypted = models.TextField(
        blank=True,
        default='',
        verbose_name='E-mail Itaú Criptografado'
    )

    itau_password_encrypted = models.TextField(
        blank=True,
        default='',
        verbose_name='Senha Itaú Criptografada'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def has_access_password(self):
        return bool(self.access_password_hash)

    def has_itau_credentials(self):
        return bool(self.itau_email_encrypted and self.itau_password_encrypted)

    def set_access_password(self, raw_password):
        self.access_password_hash = make_password(raw_password)

    def check_access_password(self, raw_password):
        if not self.access_password_hash:
            return False

        return check_password(raw_password, self.access_password_hash)

    def encrypt_value(self, value):
        if not value:
            return ''

        fernet = get_credentials_fernet()
        return fernet.encrypt(value.encode()).decode()

    def decrypt_value(self, value):
        if not value:
            return ''

        fernet = get_credentials_fernet()
        return fernet.decrypt(value.encode()).decode()

    def set_itau_credentials(self, email, password):
        self.itau_email_encrypted = self.encrypt_value(email)
        self.itau_password_encrypted = self.encrypt_value(password)

    def get_itau_email(self):
        return self.decrypt_value(self.itau_email_encrypted)

    def get_itau_password(self):
        return self.decrypt_value(self.itau_password_encrypted)

    def __str__(self):
        return 'Configurações do Sistema'
