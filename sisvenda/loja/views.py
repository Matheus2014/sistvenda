# -*- coding: utf-8 -*-

from django.shortcuts import render
from . import models
from django.http import HttpResponseRedirect
from loja.forms import *
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login 
from django.core.cache import cache
# Create your views here.


#view inicial, e redirecionar para o admin do projeto
def login(request):
	form=FormLogin()
	if request.method=="POST":
		form = FormLogin(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user)

			return HttpResponseRedirect("/admin/")
		else:
			form = FormLogin()	

	return render(request, 'login.html', {'form':form})

def cadastro(request):
	if request.method == "POST":
		form = FormCadastro(request.POST)
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect("/")
		else:	
			form = FormCadastro()
	else:
		form = FormCadastro()	
	return render(request, 'cadastro.html', {'form':form})

#view para a pagina principal
@login_required()
def admin(request):
	return render(request, 'admin/index.html', {})

#procesar venda
@login_required()
def ProssVenda(request):
	form = VendaForm()
	formitem = FormItem()
	config = Config.objects.filter(user=request.user)
	valor=0
	valorp= 0
	if request.method=="GET":
		formitem=FormItem(request.GET)
		if formitem.is_valid():
			formitem.save()
			formitem=FormItem()
		else:
			formitem=FormItem()
	if request.method=="POST":
		form = VendaForm(request.POST)
		if form.is_valid():
			venda = form.save(commit=False)
			venda.user = request.user
			venda.save()
			
			form=VendaForm(request.POST, instance=venda)

			venda2 = form.save()
			venda2.save()
			#calcula o valor total da venda com os itens
			for i in venda2.item.all():
				valor+=i.valor*i.quntidade
			item = Item.objects.filter().delete()
			pagamento = form.cleaned_data.get("pagamento")

			#seta o valor da venda
			venda.valor=valor
			venda.save()

			#ve se a venda é a vista e calcula o desconto, caso contrario calcula o valor da parcela
			if pagamento=="a_vista":
				desconto = valor*(config.por_avista/100)
				valorp=valor-desconto
				financeiro = Financeiro.objects.create(entidade=venda.cliente,valor_total=valorp,desconto=desconto,valor_parcela=0,status='A Vista',user=request.user)
				financeiro.save()			
			else:
				#link do calculo usado como base http://www.matematicadidatica.com.br/CalculoPrestacao.aspx
				taxa=config.taxa_juro/100
				qparcelas=config.quntidade_parcelas
				cf = taxa/(1-(1/((1+taxa) ** qparcelas)))
				pmt = valor*cf
				valorp=pmt*qparcelas
				financeiro = Financeiro.objects.create(entidade=venda.cliente,valor_total=valorp,valor_parcela=pmt,desconto=0,status='Parcelado',user=request.user)
				financeiro.save()

 	return render(request,'admin/venda.html',{'form':form,'formitem':formitem,'valorp':valorp})

#lista as vendas
@login_required()
def listVenda(request):
	venda = Venda.objects.filter(user=request.user)
	return render(request, 'admin/listvenda.html',{'venda':venda}) 	

#cancela venda
@login_required()
def CancelaVenda(request,id):
	venda = Venda.objects.get(pk=id).delete()
	return HttpResponseRedirect("/admin/listarvenda/")

#fim das vendas

#financeiro das vendas
@login_required()
def financeiro(request):
	fin= Financeiro.objects.filter(user=request.user)
	return render(request,'admin/financeiro.html',{'fin':fin})

@login_required()
def ClearFinanceiro(request,pk):
	fin = Financeiro.objects.get(pk=pk).delete()
	return HttpResponseRedirect("/admin/financeirovedas/")

#fim de financeiro das vendas

#procesar pedido
@login_required()
def ProssPedido(request):
	form = PedidoForm()
	formitem = FormItem()
	config = Config.objects.filter(user=request.user)
	valor=0
	valorp= 0
	if request.method=="GET":
		formitem=FormItem(request.GET)
		if formitem.is_valid():
			formitem.save()
			formitem=FormItem()
		else:
			formitem=FormItem()
	if request.method=="POST":
		form = PedidoForm(request.POST)
		if form.is_valid():
			pedido = form.save(commit=False)
			pedido.user = request.user
			pedido.save()

			form = PedidoForm(request.POST,instance=pedido)
			pedido2 = form.save()
			pedido2.save()

			#calcula o valor total do pedido com os itens
			for i in pedido2.item.all():
				valor+=i.valor*i.quntidade
			item = Item.objects.filter().delete()

			#seta o valor do pedido
			pedido.valor=valor
			pedido.save()

			financeiro = FinanceiroPedido.objects.create(entidade=pedido.fornecedor,valor_total=valor,user=request.user)
			financeiro.save()			

 	return render(request,'admin/pedido.html',{'form':form,'formitem':formitem,'valorp':valor})

#lista os pedidos
@login_required()
def listPedido(request):
	pedido = Pedido.objects.filter(user=request.user)
	return render(request, 'admin/listpedido.html',{'pedido':pedido}) 	

#cancela pedido
@login_required()
def CancelaPedido(request,id):
	pedido = Pedido.objects.get(pk=id).delete()
	return HttpResponseRedirect("/admin/listarpedidos/")

#views dos pedidos

#financeiro dos pedidos

@login_required()
def financeiroPedido(request):
	fin= FinanceiroPedido.objects.filter(user=request.user)
	return render(request,'admin/financeiropedido.html',{'fin':fin})

@login_required()
def ClearFinanceiroPedido(request,pk):
	fin = FinanceiroPedido.objects.get(pk=pk).delete()
	return HttpResponseRedirect("/admin/financeiropedidos/")

#fim dos financeiros dos pedidos

#fim dos pedidos

#config
@login_required()
def config(request):
	config=Config.objects.filter(user=request.user)
	msg=''
	if config.count()==0:
		form = FormConfig()
		if request.method=="POST":
			form = FormConfig(request.POST)		
			if form.is_valid():
				config=form.save(commit=False)
				config.user = request.user
				config.save()
				msg='dados alterados com sucesso!'
	else:
		if request.method=="POST":
			form = FormConfig(request.POST,instance=Config.objects.get(pk=1))		
			if form.is_valid():
				form.save()
				msg='dados alterados com sucesso!'
		else:
			form = FormConfig(instance=Config.objects.get(pk=1))
			

	return render(request,'admin/config.html',{'form':form,'msg':msg})

#views do cliente

#adiciona o cliente e pede algumas informaçoes iniciais
@login_required()
def addcliente(request):
	form = FormAddCliente()
	msg = ''
	if request.method=="POST":
		form = FormAddCliente(request.POST, request.FILES)

		if form.is_valid():
			cep = form.cleaned_data.get("cep")
			tipo = form.cleaned_data.get("tipo")
			descricao = form.cleaned_data.get("descricao")
			complemento = form.cleaned_data.get("complemento")
			numero = form.cleaned_data.get("numero")

			descr_email = form.cleaned_data.get("descricao_email")
			email = form.cleaned_data.get("email")

			cl = form.save(commit=False)
			cl.user=request.user
			cl.save()

			ende = EnderecoCliente.objects.create(cep=cep, tipo=tipo, descricao=descricao, complemento=complemento, numero=numero, cliente=cl)
			ende.save()
			email = EmailCliente.objects.create(descricao=descr_email, email=email, cliente=cl)
			email.save()

			msg = 'cliente cadastrado com sucesso'
			form = FormAddCliente()	
		else: 
			msg = 'deu errado'
			form = FormAddCliente()	

	return render(request, 'admin/addcliente.html', {'form':form, 'msg':msg})

#lista os clientes
@login_required()
def listCliente(request):
	cl = Cliente.objects.filter(user__username=request.user.username)
	return render(request, 'admin/listcliente.html',{'cl':cl})

#edita apenas as informaçoes do cliente
@login_required()
def editCliente(request, id):
	cl = Cliente.objects.get(pk=id)
	if request.method == "POST":
	 		form = EditCliente(request.POST, request.FILES,instance=cl)
	 		if form.is_valid():
	 			form.save()
	 			return HttpResponseRedirect("/admin/listarcliente/")
	else:
	 	form = EditCliente(instance=cl)
	return render(request, 'admin/editcliente.html', {'form':form})

#vizualiza as informações do cliente e posibilita o cadastro de novos emails, enderecos e documentos
@login_required()
def viewCliente(request, id):
	cl = Cliente.objects.get(pk=id)
	emails = EmailCliente.objects.filter(cliente__pk=id)
	enderecos = EnderecoCliente.objects.filter(cliente__pk=id)
	doc = DocumentoCliente.objects.filter(cliente__pk=id)
	formEmail = FormEmail()
	formEnde = FormEnde()
	formDoc = FormDoc()

	return render(request, 'admin/viewcliente.html',{'cl':cl, 'mail':emails,'ende':enderecos,'doc':doc,'formEmail':formEmail,'formEnde':formEnde,'formDoc':formDoc})

#adiciona um email para um cliente especifico
@login_required()
def AddEmail(request, id):
	if request.method=="POST":
		form = FormEmail(request.POST)
		if form.is_valid():
			 form.save()

	return HttpResponseRedirect("/admin/detalhecliente/"+id)

#adicionar um endereco para um cliente
@login_required()
def AddEnde(request, id):
	if request.method=="POST":
		form = FormEnde(request.POST)
		if form.is_valid():
			 form.save()

	return HttpResponseRedirect("/admin/detalhecliente/"+id)

#adicionar um documento para um cliente
@login_required()
def AddDoc(request, id):
	if request.method=="POST":
		form = FormDoc(request.POST)
		if form.is_valid():
			 form.save()

	return HttpResponseRedirect("/admin/detalhecliente/"+id)	

#exclui um cliente
@login_required()
def excluirCliente(request, pk):
	cl = Cliente.objects.get(pk=pk).delete()
	return HttpResponseRedirect('/admin/listarcliente/')

#exclui email
@login_required()
def ClearEmail(request, idemail):
	email = EmailCliente.objects.get(pk=idemail)
	idcl = email.cliente.pk
	email.delete()
	return HttpResponseRedirect("/admin/detalhecliente/%d"%idcl)

#exclui endereco
@login_required()
def ClearEnde(request, idende):
	ende = EnderecoCliente.objects.get(pk=idende)
	idcl = ende.cliente.pk
	ende.delete()
	return HttpResponseRedirect("/admin/detalhecliente/%d"%idcl)

#exclui documento
@login_required()
def ClearDoc(request, iddoc):
	doc = DocumentoCliente.objects.get(pk=iddoc)
	idcl = doc.cliente.pk
	doc.delete()
	return HttpResponseRedirect("/admin/detalhecliente/%d"%idcl)

#fim das views do cliente

#views do fornecedor

#adiciona o fornecedor e pede algumas informaçoes iniciais
@login_required()
def addFornecedor(request):
	form = FormAddFornecedor()
	msg = ''
	if request.method=="POST":
		form = FormAddFornecedor(request.POST, request.FILES)

		if form.is_valid():
			cep = form.cleaned_data.get("cep")
			tipo = form.cleaned_data.get("tipo")
			descricao = form.cleaned_data.get("descricao")
			complemento = form.cleaned_data.get("complemento")
			numero = form.cleaned_data.get("numero")

			descr_email = form.cleaned_data.get("descricao_email")
			email = form.cleaned_data.get("email")

			fornec = form.save(commit=False)
			fornec.user = request.user
			fornec.save()

			ende = EnderecoFornecedor.objects.create(cep=cep, tipo=tipo, descricao=descricao, complemento=complemento, numero=numero, fornecedor=fornec)
			ende.save()
			email = EmailFornecedor.objects.create(descricao=descr_email, email=email, fornecedor=fornec)
			email.save()

			msg = 'fornecedor cadastrado com sucesso'
			form = FormAddCliente()	
		else: 
			msg = 'deu errado'
			form = FormAddFornecedor()	

	return render(request, 'admin/addfornecedor.html', {'form':form, 'msg':msg})

#lista os fornecedores
@login_required()
def listFornecedor(request):
	fornec = Fornecedor.objects.filter(user=request.user)
	return render(request, 'admin/listfornecedor.html',{'fornec':fornec})

#edita apenas as informaçoes do fornecedor
@login_required()
def editFornecedor(request, id):
	fornec = Fornecedor.objects.get(pk=id)
	if request.method == "POST":
	 		form = EditFornecedor(request.POST, request.FILES,instance=fornec)
	 		if form.is_valid():
	 			form.save()
	 			return HttpResponseRedirect("/admin/listarfornecedor/")
	else:
	 	form = EditFornecedor(instance=fornec)
	return render(request, 'admin/editfornecedor.html', {'form':form})

#vizualiza as informações do fornecedor e posibilita o cadastro de novos emails, enderecos e documentos
@login_required()
def viewFornecedor(request, id):
	fornec = Fornecedor.objects.get(pk=id)
	emails = EmailFornecedor.objects.filter(fornecedor__pk=id)
	enderecos = EnderecoFornecedor.objects.filter(fornecedor__pk=id)
	doc = DocumentoFornecedor.objects.filter(fornecedor__pk=id)
	pro = Produto.objects.filter(fornecedor__pk=id)
	formEmail = FormEmailFornecedor()
	formEnde = FormEndeFornecedor()
	formDoc = FormDocFornecedor()
	formpro = FormEditProduto()

	return render(request, 'admin/viewfornecedor.html',{'fornec':fornec,'pro':pro,'mail':emails,'ende':enderecos,'doc':doc,'formEmail':formEmail,'formEnde':formEnde,'formDoc':formDoc,'formpro':formpro})

#adiciona um produto ao fornecedor, no detalhe do fornecedor
@login_required()
def AddProdutoFornecedor(request, id):
	if request.method=="POST":
	   form = FormEditProduto(request.POST)
	   if form.is_valid():
		  produto=form.save(commit=False)
		  produto.user=request.user
		  produto.save()

	return HttpResponseRedirect("/admin/detalhefornecedor/"+id)	   

#adiciona um email para um fornecedor especifico
@login_required()
def AddEmailFornecedor(request, id):
	if request.method=="POST":
		form = FormEmailFornecedor(request.POST)
		if form.is_valid():
			 form.save()

	return HttpResponseRedirect("/admin/detalhefornecedor/"+id)



#adicionar um endereco para um fornecedor
@login_required()
def AddEndeFornecedor(request, id):
	if request.method=="POST":
		form = FormEndeFornecedor(request.POST)
		if form.is_valid():
			 form.save()

	return HttpResponseRedirect("/admin/detalhefornecedor/"+id)

#adicionar um documento para um fornecedor
@login_required()
def AddDocFornecedor(request, id):
	if request.method=="POST":
		form = FormDocFornecedor(request.POST)
		if form.is_valid():
			 form.save()

	return HttpResponseRedirect("/admin/detalhefornecedor/"+id)	

#exclui um fornecedor
@login_required()
def excluirFornecedor(request, pk):
	fornec = Fornecedor.objects.get(pk=pk).delete()
	return HttpResponseRedirect('/admin/listarfornecedor/')

#exclui email
@login_required()
def ClearEmailFornecedor(request, idemail):
	email = EmailFornecedor.objects.get(pk=idemail)
	idfornec = email.fornecedor.pk
	email.delete()
	return HttpResponseRedirect("/admin/detalhefornecedor/%d"%idfornec)

#exclui endereco
@login_required()
def ClearEndeFornecedor(request, idende):
	ende = EnderecoFornecedor.objects.get(pk=idende)
	idfornec = ende.fornecedor.pk
	ende.delete()
	return HttpResponseRedirect("/admin/detalhefornecedor/%d"%idfornec)

#exclui documento
@login_required()
def ClearDocFornecedor(request, iddoc):
	doc = DocumentoFornecedor.objects.get(pk=iddoc)
	idfornec = doc.fornecedor.pk
	doc.delete()
	return HttpResponseRedirect("/admin/detalhefornecedor/%d"%idfornec)

#fim das views do fornecedor

#views do produto

#cadastra produto
@login_required()
def AddProduto(request):
	form = FormAddProduto()
	msg=''
	if request.method=="POST":
		form = FormAddProduto(request.POST, request.FILES)
		if form.is_valid():
			descricao = form.cleaned_data.get("descricao")
			fator = form.cleaned_data.get("fator")

			produto = form.save(commit=False)
			produto.user = request.user
			produto.save()

			unidade = Unidade.objects.create(descricao=descricao, fator=fator, produto=produto)
			unidade.save()

			form = FormAddProduto()

			msg = 'Produto cadastrado com sucesso'
		else:
			msg = 'algo deu errado'
				
	return render(request, 'admin/addproduto.html',{'form':form, 'msg':msg})		

#lista todos os produtos
@login_required()
def ListProduto(request):
	pro= Produto.objects.filter(user=request.user)
	return render(request, 'admin/listproduto.html',{'pro':pro})

#edita apenas as informaçoes do produto
@login_required()
def editProduto(request, id):
	pro = Produto.objects.get(pk=id)
	if request.method == "POST":
	 		form = FormEditProduto(request.POST, request.FILES,instance=pro)
	 		if form.is_valid():
	 			form.save()
	 			return HttpResponseRedirect("/admin/listarproduto/")
	else:
	 	form = FormEditProduto(instance=pro)
	return render(request, 'admin/editproduto.html', {'form':form})

#exclui um produto
@login_required()
def excluirProduto(request, pk):
	pro = Produto.objects.get(pk=pk).delete()
	return HttpResponseRedirect('/admin/listarproduto/')

#vizualiza as informações do roduto e permite o cadastro de novas unidades
@login_required()
def viewProduto(request, id):
	pro = Produto.objects.get(pk=id)
	fator = Unidade.objects.filter(produto__pk=id)
	form = FormUnidade()

	return render(request, 'admin/viewproduto.html',{'pro':pro,'fator':fator,'form':form})

#adicionar uma unidade para um produto
@login_required()
def AddUni(request, id):
	if request.method=="POST":
		form = FormUnidade(request.POST)
		if form.is_valid():
			 form.save()

	return HttpResponseRedirect("/admin/detalheproduto/"+id)

@login_required()
def ClearUni(request, id):
	uni = Unidade.objects.get(pk=id)
	idpro = uni.produto.pk
	uni.delete()
	return HttpResponseRedirect("/admin/detalheproduto/%d"%idpro)

def sair(request):
	logout(request)
	return HttpResponseRedirect("/")		