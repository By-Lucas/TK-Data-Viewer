import django_filters
from django import forms
from django.db.models import Q

from costumers.models import City, Proposal
from costumers.models import Prefessions


class ProposalFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter',
                                       widget=forms.TextInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'CPF/CNPJ, Clínica, Nome ou Proposta'})
                                       )

    created_start_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Data inicial de criação'
    )
    created_end_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Data final de criação'
    )
    class Meta:
        model = Proposal
        fields = ('clinic__business_name', 'proponent__name', 'proponent__cnpj_cpf', 'protocol')

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(clinic__business_name__icontains=value) |
            Q(proponent__cnpj_cpf__icontains=value) |
            Q(proponent__name__icontains=value) |
            Q(protocol__icontains=value)
        )


class CityFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(label="Nome da cidade", lookup_expr='icontains', widget=forms.TextInput(
        attrs={
            'class': 'form-control', 'placeholder': 'Digite o nome da cidade'
        }
    ))

    class Meta:
        model = City
        fields = ['uf', 'city']


class PrefessionsFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(label="Nome da profissão", lookup_expr='icontains', widget=forms.TextInput(
        attrs={
            'class': 'form-control', 'placeholder': 'Digite o nome da cidade'
        }
    ))

    class Meta:
        model = Prefessions
        fields = ['description']
