# -*- coding: utf-8 -*-

from django import forms
from django.forms import CharField, Form, PasswordInput,ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *

#formulario para login, com o metodo save fazendo a autenticacao do usuario
class FormLogin(forms.Form):
	username = forms.CharField(label='Username',required=True)
	senha = forms.CharField(label='Senha',required=True, widget=forms.PasswordInput())

	def clean_username(self):
		username = self.cleaned_data.get("username")
		if not User.objects.filter(username=username):
			raise forms.ValidationError("Username nao encontrado")
		return username

	def clean_senha(self):
		username = self.cleaned_data.get("username")
		senha = self.cleaned_data.get("senha")

		if not authenticate(username=username, password=senha):
			raise forms.ValidationError("Username nao encontrado")
		return senha

	def save(self):
		username = self.cleaned_data.get("username")
		senha = self.cleaned_data.get("senha")	 		
		return authenticate(username=username, password=senha)

class FormAddCliente(forms.ModelForm):
	class Meta:
		model=Cliente
		exclude = ['ativo',]

	descricao_email = forms.CharField(label='Descrição do email', max_length=200)
	email = forms.EmailField(label='Email')

	cep = forms.CharField(label='Cep',max_length=30)
	tipo = forms.CharField(label='Tipo do endereço', max_length=50)
	descricao = forms.CharField(label='Descrição do endereço', max_length=200) 
	complemento = forms.CharField(label='Complemento', max_length=200) 
	numero = forms.CharField(label='Numero do endereço', max_length=10)	

