from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from helpers import commons
from accounts.others_models.model_user_clinic import UserClinic


def admin_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.user_clipse or request.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response

        try:
            user_clinic_permission = UserClinic.objects.get(user=request.user, user__is_active=True)

        except:
            user_clinic_permission = UserClinic.objects.filter(user=request.user, user__is_active=True).first()

        if user_clinic_permission.user.permission == commons.ADMINISTRATOR:
            response = view_func(request, *args, **kwargs)
            return response

        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso'))
            return redirect('home')

    return wraps(view_func)(_decorator)


def register_user_level_required(view_func):
    def _decorator(request, *args, **kwargs):

        is_PJ = False

        if request.user.user_clipse or request.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response

        if request.user.permission == commons.CLIPSE_AGENT or request.user.permission == commons.CLIPSE_SELLER:
            if len(request.user.cnpj_cpf) == 18:
                is_PJ = True

        try:
            user_clinic_permission = UserClinic.objects.get(user=request.user, user__is_active=True)

        except:
            user_clinic_permission = UserClinic.objects.filter(user=request.user, user__is_active=True).first()

        if user_clinic_permission.user.permission == commons.ADMINISTRATOR or is_PJ:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso'))
            return redirect('home')

    return wraps(view_func)(_decorator)


def admin_clipse_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.user_clipse or request.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response

        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso.'))
            return redirect('home')

    return wraps(view_func)(_decorator)


def customer_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.user_clipse or request.user.is_superuser:
            response = view_func(request, *args, **kwargs)
            return response
        try:
            user_clinic_permission = UserClinic.objects.get(user=request.user, user__is_active=True)

        except UserClinic.MultipleObjectsReturned or UserClinic.DoesNotExist:
            user_clinic_permission = UserClinic.objects.filter(user=request.user, user__is_active=True).first()

        if user_clinic_permission.user.permission == commons.ADMINISTRATOR or \
                user_clinic_permission.user.permission == commons.COMMOM_USER:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            messages.warning(request, _('Você não tem permissão pra acessar o recurso.'))
            return redirect('home')

    return wraps(view_func)(_decorator)

def proposal_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        if request.user.user_clipse or request.user.is_superuser:
           if request.POST.get("status") != 'PR':
              response = view_func(request, *args, **kwargs)
              return response
           else:
              messages.warning(request, _('Usuário sem permissão para editar/reenviar proposta.'))
              return redirect('')

        try:
            user_clinic_permission = UserClinic.objects.get(user=request.user, user__is_active=True)

        except UserClinic.MultipleObjectsReturned or UserClinic.DoesNotExist:
            user_clinic_permission = UserClinic.objects.filter(user=request.user, user__is_active=True).first()

        if user_clinic_permission.user.permission == commons.ADMINISTRATOR or \
           user_clinic_permission.user.permission == commons.COMMOM_USER:
            if request.POST.get("status") == 'CR':
               response = view_func(request, *args, **kwargs)
               return response
            else:
               messages.warning(request, _('Usuário sem permissão para editar/reenviar proposta.'))
               return redirect('') 
        else:
            messages.warning(request, _('Usuário sem permissão para editar/reenviar proposta.'))
            return redirect('')

    return wraps(view_func)(_decorator)