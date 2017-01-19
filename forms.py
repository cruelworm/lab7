# -*- coding: utf-8 -*-

from django import forms
from .models import OfficesModel, MembersModel
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label=u'Логин'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=u'Пароль'
    )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username = data.get('username', ''), password = data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user

        else:
            raise forms.ValidationError(u'Неверная пара логин/пароль!')


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=5,
        max_length=30,
        label=u'Логин'
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        label=u'Имя'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        label=u'Фамилия'
    )



    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        label=u'E-mail'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        label=u'Пароль'
    )
    password_check= forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        label=u'Повторите пароль'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError(u'Пользователь с таким логинм уже существует')
        except User.DoesNotExist:
            return username

    def clean(self):
        p1 = self.cleaned_data.get('password', '')
        p2 = self.cleaned_data.get('password_check','')

        if p1 != p2:
            raise forms.ValidationError(u'Введённые пароли не совпадают')

    def save(self):
        data = self.cleaned_data
        password = data.get('password')
        u = User()

        u.username = data.get('username')
        u.password = make_password(password)
        u.email = data.get('email')
        u.first_name = data.get('first_name')
        u.last_name = data.get('last_name')

        u.is_active = True
        u.is_superuser = False
        u.save()

        test = MembersModel()
        test.user_id = u.id
        test.l_name = u.last_name
        test.f_name = u.first_name
        test.save()

        return authenticate(username=u.username, password=password)


class OfficeForm(forms.ModelForm):

    class Meta:
        model = OfficesModel
        fields = ('named', 'location', 'picture')


class MemberForm(forms.ModelForm):

    class Meta:
        model = MembersModel
        fields = ('l_name', 'f_name','position', 'office')


class CreateForm(forms.Form):
    named = forms.CharField(label='Название', required=False)
    location = forms.CharField(label='Адрес', required=False)
    picture = forms.ImageField(label='Логотип', required=False)

class Create(forms.ModelForm):
    class Meta:
        model = OfficesModel
        fields = ['named', 'location', 'picture']
        labels = {
            'named': _('Название'),
            'location': _('Адрес'),
            'picture': _('Логотип')
        }
