# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Estrutura do Cliente

class Cliente(models.Model):
	nome = models.CharField(verbose_name='Nome do cliente', max_length=100 )
	foto = models.FileField(verbose_name='Foto do cliente', upload_to='/cliente/', blank=True )
	ativo = models.BooleanField(verbose_name='Ativo', blank=True, default=True)

	def __unicode__(self):
		return self.nome

class EnderecoCliente(models.Model):
	cep = models.CharField(verbose_name='Cep',max_length=30)
	tipo = models.CharField(verbose_name='Tipo do endereço', max_length=50)
	descricao = models.CharField(verbose_name='Descrição do endereço', max_length=200) 
	complemento = models.CharField(verbose_name='Complemento', max_length=200) 
	numero = models.CharField(verbose_name='Numero do endereço', max_length=10)
	ativo = models.BooleanField(verbose_name='Ativo', blank=True, default=True)
	cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)

	def __unicode__(self):
		return self.numero 

class EmailCliente(models.Model):
	descricao = models.CharField(verbose_name='Descrição do email', blank=True, max_length=200)
	email = models.EmailField(unique=True)
	ativo = models.BooleanField(verbose_name='Ativo', blank=True, default=True)
	cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)


	def __unicode__(self):
		return self.email

class DocumentoCliente(models.Model):
	numero = models.CharField(verbose_name='Numero do docuemento', max_length=10)
	tipo = models.CharField(verbose_name='Tipo do documento', max_length=50)
	emissao = models.DateField(verbose_name='Data de Emissão')
	vencimento = models.DateField(verbose_name='Data de Vencimento')		
	ativo = models.BooleanField(verbose_name='Ativo', blank=True, default=True)
	cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
		
	def __unicode__(self):
		return self.numero	

	