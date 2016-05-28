# -*- coding: utf-8 -*-

from django import forms
from django.forms import CharField, Form, PasswordInput,ModelForm
from django.contrib.auth import authenticate
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

class FormCadastro(forms.ModelForm):
	senha = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput())		
	senha2 = forms.CharField(label='Confirmar Senha', required=True, widget=forms.PasswordInput())

	class Meta():
		model= User
		fields = ['username','email','name','foto']

	def clean_senha2(self):
		senha = self.cleaned_data.get("senha")
		senha2 = self.cleaned_data.get("senha2")

		if senha and senha2 and senha != senha2:
			raise forms.ValidationError("Passwords don't match")
		return senha2
		
	def save(self, commit=True):
		
		user = super(FormCadastro, self).save(commit=False)
		user.set_password(self.cleaned_data.get("senha"))
		if commit:
			user.save()
		return user	


#forms do cliente
class FormAddCliente(forms.ModelForm):
	class Meta:
		model=Cliente
		exclude = ['ativo','user']

	descricao_email = forms.CharField(label='Descrição do email', max_length=200)
	email = forms.EmailField(label='Email')

	cep = forms.CharField(label='Cep',max_length=30)
	tipo = forms.CharField(label='Tipo do endereço', max_length=50)
	descricao = forms.CharField(label='Descrição do endereço', max_length=200) 
	complemento = forms.CharField(label='Complemento', max_length=200) 
	numero = forms.CharField(label='Numero do endereço', max_length=10)	

class EditCliente(forms.ModelForm):
	class Meta:
		model=Cliente
		exclude = ['ativo',]

class FormEmail(forms.ModelForm):
	class Meta:
		model= EmailCliente
		exclude = ['ativo',]

class FormEnde(forms.ModelForm):
	class Meta:
		model= EnderecoCliente
		exclude = ['ativo',]

class FormDoc(forms.ModelForm):
	class Meta:
		model= DocumentoCliente
		exclude = ['ativo',]

#fim dos forms do cliente
#forms do fornecedor

class FormAddFornecedor(forms.ModelForm):
	class Meta:
		model=Fornecedor
		exclude = ['ativo','user']

	descricao_email = forms.CharField(label='Descrição do email', max_length=200)
	email = forms.EmailField(label='Email')

	cep = forms.CharField(label='Cep',max_length=30)
	tipo = forms.CharField(label='Tipo do endereço', max_length=50)
	descricao = forms.CharField(label='Descrição do endereço', max_length=200) 
	complemento = forms.CharField(label='Complemento', max_length=200) 
	numero = forms.CharField(label='Numero do endereço', max_length=10)	

class EditFornecedor(forms.ModelForm):
	class Meta:
		model=Fornecedor
		exclude = ['ativo',]

class FormEmailFornecedor(forms.ModelForm):
	class Meta:
		model= EmailFornecedor
		exclude = ['ativo',]

class FormEndeFornecedor(forms.ModelForm):
	class Meta:
		model= EnderecoFornecedor
		exclude = ['ativo',]

class FormDocFornecedor(forms.ModelForm):
	class Meta:
		model= DocumentoFornecedor
		exclude = ['ativo',]

#fim dos forms do fornecedor
#forms do produto

class FormAddProduto(forms.ModelForm):
	class Meta:
		model=Produto
		exclude = ['user']	

	descricao = forms.CharField(label="Descrição da unidade")
	fator = forms.IntegerField(label="Fator")	

class FormEditProduto(forms.ModelForm):
	class Meta:
		model=Produto
		fields = '__all__'
			
class FormUnidade(forms.ModelForm):
	class Meta:
		model=Unidade
		fields= '__all__'

#fim dos forms do produto
#forms da venda

class VendaForm(forms.ModelForm):
	op=(
		('parcelado','Parcelado'),
		('a_vista','A Vista'),
		)
	pagamento = forms.ChoiceField(choices=op)
	class Meta:
		model=Venda
		exclude=['valor','user']

class FormItem(forms.ModelForm):
	class Meta:
		model = Item
		fields='__all__'

#fim dos forms da venda

#forms dos pedidos

class PedidoForm(forms.ModelForm):
	class Meta:
		model=Pedido
		exclude=['valor','data','user']

#fim dos forms dos pedidos

#form config
class FormConfig(forms.ModelForm):
	class Meta:
		model=Config
		exclude=['user']
