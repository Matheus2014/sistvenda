from django.shortcuts import render
from . import models
from django.http import HttpResponseRedirect
from loja.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login 
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

@login_required()
def admin(request):
	return render(request, 'admin/index.html', {})

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

@login_required()
def listCliente(request):
	cl = Cliente.objects.all()
	return render(request, 'admin/listcliente.html',{'cl':cl})

def sair(request):
	logout(request)
	return HttpResponseRedirect("/")		