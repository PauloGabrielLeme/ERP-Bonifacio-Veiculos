# cars/forms.py

from decimal import Decimal, InvalidOperation
from django import forms
from .models import (
    Car,
    Sale,
    VehicleDocument,
    IPVA,
    Contract,
    InvoiceDocument,
)


def parse_brazilian_decimal(value):
    """
    Converte valores monetários para Decimal.

    Aceita:
    "40000"      -> Decimal("40000.00")
    "40000,00"   -> Decimal("40000.00")
    "40.000,00"  -> Decimal("40000.00")
    "40000.00"   -> Decimal("40000.00")
    "R$ 40.000,00" -> Decimal("40000.00")
    """
    if value in [None, '']:
        return Decimal('0.00')

    if isinstance(value, Decimal):
        return value

    value = str(value).strip()
    value = value.replace('R$', '').replace(' ', '')

    if not value:
        return Decimal('0.00')

    if ',' in value:
        value = value.replace('.', '').replace(',', '.')

    try:
        return Decimal(value)
    except InvalidOperation:
        raise forms.ValidationError(
            'Informe um valor válido. Exemplo: 40000,00 ou 40.000,00.'
        )


class CarForm(forms.ModelForm):
    purchase_price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '40000,00',
            'class': 'form-control money-input'
        })
    )

    sale_price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '50000,00',
            'class': 'form-control money-input'
        })
    )

    fipe_initial_price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '50000,00',
            'class': 'form-control money-input',
            'id': 'fipe_initial_price'
        })
    )

    fipe_current_price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '40000,00',
            'class': 'form-control money-input',
            'id': 'fipe_current_price'
        })
    )

    class Meta:
        model = Car

        fields = [
            'brand',
            'model',
            'year',
            'plate',
            'color',
            'mileage',
            'purchase_price',
            'sale_price',
            'status',
            'publication_sites',
            'image',

            'needs_cleaning',
            'needs_sanitizing',
            'has_spare_key',
            'has_cautelar',
            'has_procuracao',
            'has_crlv',

            'ad_olx',
            'ad_webmotors',
            'ad_icarros',
            'ad_mercado_livre',
            'ad_facebook',
            'ad_instagram',
            'other_ad_sites',

            'fipe_code',
            'fipe_initial_price',
            'fipe_current_price',

            'observations',
        ]

        widgets = {
            'brand': forms.TextInput(attrs={
                'placeholder': 'Selecione a marca',
                'class': 'form-control'
            }),

            'model': forms.TextInput(attrs={
                'placeholder': 'Selecione o modelo',
                'class': 'form-control'
            }),

            'year': forms.NumberInput(attrs={
                'placeholder': 'Ano',
                'class': 'form-control'
            }),

            'plate': forms.TextInput(attrs={
                'placeholder': 'Ex: ABC-1234/ABC1D23',
                'class': 'form-control'
            }),

            'color': forms.TextInput(attrs={
                'placeholder': 'Branco',
                'class': 'form-control'
            }),

            'mileage': forms.NumberInput(attrs={
                'placeholder': '50000',
                'class': 'form-control'
            }),

            'status': forms.Select(attrs={
                'class': 'form-control'
            }),

            'publication_sites': forms.TextInput(attrs={
                'placeholder': 'Ex: OLX, WebMotors...',
                'class': 'form-control'
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'needs_cleaning': forms.Select(attrs={
                'class': 'form-control'
            }),

            'needs_sanitizing': forms.Select(attrs={
                'class': 'form-control'
            }),

            'has_spare_key': forms.Select(attrs={
                'class': 'form-control'
            }),

            'has_cautelar': forms.Select(attrs={
                'class': 'form-control'
            }),

            'has_procuracao': forms.Select(attrs={
                'class': 'form-control'
            }),

            'has_crlv': forms.Select(attrs={
                'class': 'form-control'
            }),

            'ad_olx': forms.CheckboxInput(attrs={
                'class': 'checkbox-control'
            }),

            'ad_webmotors': forms.CheckboxInput(attrs={
                'class': 'checkbox-control'
            }),

            'ad_icarros': forms.CheckboxInput(attrs={
                'class': 'checkbox-control'
            }),

            'ad_mercado_livre': forms.CheckboxInput(attrs={
                'class': 'checkbox-control'
            }),

            'ad_facebook': forms.CheckboxInput(attrs={
                'class': 'checkbox-control'
            }),

            'ad_instagram': forms.CheckboxInput(attrs={
                'class': 'checkbox-control'
            }),

            'other_ad_sites': forms.TextInput(attrs={
                'placeholder': 'Nome do site...',
                'class': 'form-control'
            }),

            'fipe_code': forms.TextInput(attrs={
                'placeholder': 'Ex: 004219-1',
                'class': 'form-control'
            }),

            'observations': forms.Textarea(attrs={
                'placeholder': 'Adicione observações sobre o veículo, manutenções, documentação, histórico, etc...',
                'class': 'form-control observations-textarea',
            }),
        }

    def clean_purchase_price(self):
        return parse_brazilian_decimal(self.cleaned_data.get('purchase_price'))

    def clean_sale_price(self):
        return parse_brazilian_decimal(self.cleaned_data.get('sale_price'))

    def clean_fipe_initial_price(self):
        return parse_brazilian_decimal(self.cleaned_data.get('fipe_initial_price'))

    def clean_fipe_current_price(self):
        return parse_brazilian_decimal(self.cleaned_data.get('fipe_current_price'))


class SaleForm(forms.ModelForm):
    sale_price = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '50000,00',
            'class': 'form-control money-input'
        })
    )

    class Meta:
        model = Sale

        fields = [
            'car',
            'sale_date',
            'sale_price',
            'payment_method',
            'buyer_type',
            'buyer_name',
            'cpf',
            'rg',
            'address',
            'phone',
            'email',
            'observations',
        ]

        widgets = {
            'car': forms.Select(attrs={
                'class': 'form-control'
            }),

            'sale_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'payment_method': forms.TextInput(attrs={
                'placeholder': 'Ex: À vista, Financiamento, etc.',
                'class': 'form-control'
            }),

            'buyer_type': forms.RadioSelect(
                choices=Sale.BUYER_TYPE_CHOICES
            ),

            'buyer_name': forms.TextInput(attrs={
                'placeholder': 'João da Silva',
                'class': 'form-control'
            }),

            'cpf': forms.TextInput(attrs={
                'placeholder': '000.000.000-00',
                'class': 'form-control'
            }),

            'rg': forms.TextInput(attrs={
                'placeholder': '00.000.000-0',
                'class': 'form-control'
            }),

            'address': forms.TextInput(attrs={
                'placeholder': 'Rua, número, bairro, cidade',
                'class': 'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'placeholder': '(00) 00000-0000',
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'email@exemplo.com',
                'class': 'form-control'
            }),

            'observations': forms.Textarea(attrs={
                'placeholder': 'Observações sobre a venda...',
                'class': 'form-control textarea-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['car'].queryset = Car.objects.filter(
            status='estoque',
            sales__isnull=True
        ).distinct().order_by('brand', 'model', 'year')

        self.fields['car'].empty_label = 'Selecione o carro'

    def clean_sale_price(self):
        return parse_brazilian_decimal(self.cleaned_data.get('sale_price'))


class IPVAForm(forms.ModelForm):
    total_value = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control money-input',
            'placeholder': '1200,00'
        })
    )

    class Meta:
        model = IPVA

        fields = [
            'car',
            'year',
            'installments',
            'total_value',
            'observations',
        ]

        widgets = {
            'car': forms.Select(attrs={
                'class': 'form-control'
            }),

            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2026'
            }),

            'installments': forms.Select(attrs={
                'class': 'form-control'
            }),

            'observations': forms.Textarea(attrs={
                'class': 'form-control textarea-control',
                'placeholder': 'Observações sobre o IPVA...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['car'].queryset = Car.objects.all().order_by(
            'brand',
            'model',
            'year'
        )
        self.fields['car'].empty_label = 'Selecione o carro'

    def clean_total_value(self):
        return parse_brazilian_decimal(self.cleaned_data.get('total_value'))


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            'widget',
            MultipleFileInput(attrs={
                'multiple': True,
                'class': 'form-control'
            })
        )
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [
                super(MultipleFileField, self).clean(file, initial)
                for file in data
            ]

        return [super().clean(data, initial)]


class VehicleDocumentForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = VehicleDocument

        fields = [
            'car',
            'document_type',
            'name',
            'notes',
            'images',
        ]

        widgets = {
            'car': forms.Select(attrs={
                'class': 'form-control'
            }),

            'document_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: CRLV_2026',
                'class': 'form-control'
            }),

            'notes': forms.Textarea(attrs={
                'placeholder': 'Adicione observações sobre o documento...',
                'class': 'form-control textarea-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['car'].queryset = Car.objects.all().order_by(
            'brand',
            'model',
            'year'
        )
        self.fields['car'].empty_label = 'Selecione o carro'
        self.fields['document_type'].empty_label = 'Selecione o tipo'


class ContractForm(forms.ModelForm):
    images = MultipleFileField(required=False)

    class Meta:
        model = Contract

        fields = [
            'car',
            'name',
            'notes',
            'images',
        ]

        widgets = {
            'car': forms.Select(attrs={
                'class': 'form-control'
            }),

            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Contrato de compra e venda',
                'class': 'form-control'
            }),

            'notes': forms.Textarea(attrs={
                'placeholder': 'Observações sobre o contrato...',
                'class': 'form-control textarea-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['car'].queryset = Car.objects.all().order_by(
            'brand',
            'model',
            'year'
        )
        self.fields['car'].empty_label = 'Selecione o carro'


class InvoiceDocumentForm(forms.ModelForm):
    typed_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control textarea-control invoice-textarea',
            'placeholder': 'Digite aqui o texto da nota fiscal...',
        })
    )

    uploaded_docx = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.docx'
        })
    )

    class Meta:
        model = InvoiceDocument

        fields = [
            'car',
            'title',
            'typed_text',
            'uploaded_docx',
        ]

        widgets = {
            'car': forms.Select(attrs={
                'class': 'form-control'
            }),

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Nota fiscal Corolla 2026'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['car'].queryset = Car.objects.all().order_by(
            'brand',
            'model',
            'year'
        )
        self.fields['car'].empty_label = 'Selecione o carro'

    def clean(self):
        cleaned_data = super().clean()

        typed_text = cleaned_data.get('typed_text')
        uploaded_docx = cleaned_data.get('uploaded_docx')

        if not typed_text and not uploaded_docx:
            raise forms.ValidationError(
                'Digite um texto ou envie um arquivo .docx.'
            )

        if typed_text and uploaded_docx:
            raise forms.ValidationError(
                'Escolha apenas uma opção: digitar texto ou enviar .docx.'
            )

        if uploaded_docx:
            filename = uploaded_docx.name.lower()

            if not filename.endswith('.docx'):
                raise forms.ValidationError(
                    'Envie apenas arquivos no formato .docx.'
                )

        return cleaned_data

class AccessPasswordCreateForm(forms.Form):
    new_password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite uma senha de proteção',
            'class': 'form-control'
        })
    )


class CredentialsUnlockForm(forms.Form):
    access_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite a senha',
            'class': 'form-control'
        })
    )


class ItauCredentialsForm(forms.Form):
    itau_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@exemplo.com',
            'class': 'form-control'
        })
    )

    itau_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha do Itaú',
            'class': 'form-control'
        })
    )


class ChangeAccessPasswordForm(forms.Form):
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha atual',
            'class': 'form-control'
        })
    )

    new_password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite a nova senha',
            'class': 'form-control'
        })
    )
