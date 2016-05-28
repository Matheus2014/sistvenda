# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models



#estrutura usuario
class UserManager(BaseUserManager):
	def create_user(self, username, email, password=None):

		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(username=username, email=self.normalize_email(email))
		user.set_password(password)
		user.save(using=self._db)
		return user 

	def create_superuser(self, username, email, password):

			user = self.create_user(username, email=email ,password=password)
			user.is_admin = True
			user.save(using=self._db)
			return user	

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(verbose_name = 'Username', max_length=50, unique=True)
	email = models.EmailField(verbose_name = 'Email', unique=True)
	foto = models.ImageField(verbose_name='Foto do Usuaurio', upload_to='user/', blank=True, default='user/sem.png' )
	name = models.CharField(verbose_name='Nome', max_length=100, blank=True)
	id = models.AutoField(primary_key=True)
	is_active = models.BooleanField(blank=True, default=True)
	is_admin = models.BooleanField(blank=True, default=False)
	date_joined = models.DateTimeField(auto_now_add=True)

	objects= UserManager()

	USERNAME_FIELD= 'username'
	REQUIRED_FIELDS= ['email']

	def __unicode__(self):
		return self.username

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	@property	
	def is_staff(self):
		return self.is_admin				


#configuração

class Config(models.Model):
	quntidade_parcelas=models.IntegerField(verbose_name="Quantidade de Parcelas", default=5,blank=True)
	taxa_juro = models.DecimalField(verbose_name="Taxa de Juro ao mes",max_digits=5,decimal_places=2,default=5,blank=True)
	por_avista = models.DecimalField(verbose_name="Porcentagem de Desconto a vista",max_digits=5,decimal_places=2,default=10,blank=True)
	user = models.ForeignKey(User)

# Estrutura do Cliente

class Cliente(models.Model):

	sexo = (
			  ('masculino','Masculino'),
			  ('feminino','Feminino'),
			  ('outro','Outro'),
			)

	nome = models.CharField(verbose_name='Nome do cliente', max_length=100 )
	foto = models.ImageField(verbose_name='Foto do cliente', upload_to='cliente/', blank=True, default='cliente/sem.png' )
	idade = models.IntegerField()
	sexo = models.CharField(max_length=20, choices=sexo)
	ativo = models.BooleanField(verbose_name='Ativo', blank=True, default=True)
	user = models.ForeignKey(User, blank=True, default=None)	

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

#fim da estrurura do cliente

#inicio da estrutura do fornecedor

class Fornecedor(models.Model):
	nome = models.CharField(verbose_name="Nome do fornecedor",max_length=100)
	foto = models.ImageField(verbose_name='Foto do cliente', upload_to='fornecedor/', blank=True, default='fornecedor/sem.png' )
	ativo = models.BooleanField(verbose_name="esta ativo?",blank=True, default=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.nome

class EnderecoFornecedor(models.Model):
	cep = models.CharField(verbose_name='Cep',max_length=30)
	tipo = models.CharField(verbose_name='Tipo do endereço', max_length=50)
	descricao = models.CharField(verbose_name='Descrição do endereço', max_length=200) 
	complemento = models.CharField(verbose_name='Complemento', max_length=200) 
	numero = models.CharField(verbose_name='Numero do endereço', max_length=10)
	ativo = models.BooleanField(verbose_name='Ativo', blank=True, default=True)
	fornecedor = models.ForeignKey(Fornecedor, on_delete = models.CASCADE)

	def __unicode__(self):
		return self.numero 

class EmailFornecedor(models.Model):
	descricao = models.CharField(verbose_name='Descrição do email', blank=True, max_length=200)
	email = models.EmailField(unique=True)
	ativo = models.BooleanField(verbose_name='Ativo', blank=True, default=True)
	fornecedor = models.ForeignKey(Fornecedor, on_delete = models.CASCADE)


	def __unicode__(self):
		return self.email

class DocumentoFornecedor(models.Model):
	numero = models.CharField(verbose_name='Numero do docuemento', max_length=10)
	tipo = models.CharField(verbose_name='Tipo do documento', max_length=50)
	emissao = models.DateField(verbose_name='Data de Emissão')
	vencimento = models.DateField(verbose_name='Data de Vencimento')		
	ativo = models.BooleanField(verbose_name='Ativo', blank=True, default=True)
	fornecedor = models.ForeignKey(Fornecedor, on_delete = models.CASCADE)
		
	def __unicode__(self):
		return self.numero

#fim da estrutura do fornecedor
#inicio da estrutura do produto

class Produto(models.Model):
	produto = models.CharField(verbose_name="Produto",max_length=20)
	foto = models.ImageField(verbose_name='Foto do cliente', upload_to='produto/', blank=True, default='produto/sem.png')
	descricao_produto = models.CharField(verbose_name="Descrição do produto", max_length=100, blank=True)
	estoque = models.IntegerField(verbose_name="Quantos no Estoque")
	fornecedor = models.ForeignKey(Fornecedor, on_delete= models.CASCADE)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.produto	

class Unidade(models.Model):
	descricao = models.CharField(verbose_name="Descrição da Unidade", max_length=50, blank=True)
	fator = models.IntegerField(verbose_name="Fator")
	produto = models.ForeignKey(Produto, on_delete = models.CASCADE)

#fim da estrutura do produto

#estrutura da venda

class Item(models.Model):
	produto= models.ForeignKey(Produto, on_delete=models.CASCADE) 
	quntidade=models.IntegerField(verbose_name="Quantidade")
	valor = models.DecimalField(max_digits=9,decimal_places=2)

	def __unicode__(self):
		return self.produto.produto

class Venda(models.Model):
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	item = models.ManyToManyField(Item)
	valor = models.DecimalField(max_digits=9,decimal_places=2, blank=True,default=0)
	user = models.ForeignKey(User)

#fim da estrutura das vendas
#estrutura do financeiro vendas

class Financeiro(models.Model):
	entidade = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	valor_parcela = models.DecimalField(max_digits=10,decimal_places=3, verbose_name="Valor da parcela",blank=True)
	valor_total = models.DecimalField(max_digits=10,decimal_places=3, verbose_name="Valor Total")
	desconto = models.DecimalField(max_digits=5,decimal_places=2,blank=True)
	status = models.CharField(max_length=20,verbose_name="Status do financeiro")
	user = models.ForeignKey(User)

#fim da estrutura do financeiro

#estrutura de pedidos

class Pedido(models.Model):
	fornecedor= models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
	data = models.DateTimeField(verbose_name = 'Data',auto_now = False, auto_now_add = True)
	valor = models.DecimalField(max_digits=9,decimal_places=2, blank=True,default=0)
	item = models.ManyToManyField(Item)
	user = models.ForeignKey(User)

class FinanceiroPedido(models.Model):
	entidade = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
	data = models.DateTimeField(verbose_name = 'Data',auto_now = False, auto_now_add = True)
	valor_total = models.DecimalField(max_digits=10,decimal_places=3, verbose_name="Valor Total")
	user = models.ForeignKey(User)

#fim da estrutura de pedidos
