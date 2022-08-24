from django.forms.models import model_to_dict
from django.views import generic
from django.template.response import TemplateResponse
from django.contrib import messages
from lista_presentes_app.models import Convidados, Presentes, PresentesConvidados, VwResultadosProdutos
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import F
from django.contrib.auth import authenticate, login, logout

def index(request):
    #if request.method == "GET":
    if request.method == "POST":

        telefone = request.POST['telefone']
        chave = request.POST['chave']

        try:
            convidado = Convidados.objects.get(telefone=telefone)
            if chave.lower().strip() != "teo2022":
                messages.error(request, "Chave de acesso inválida. Entre em contato com os papais do Téo para resolver esse problema" )
                response = TemplateResponse(request, 'lista_presentes_app/index.html', {})
                return response
            else:
                #messages.success(request, "Convidado localizado!" )
                request.session['convidado'] = model_to_dict( convidado )
                
                return redirect('opcoes')

        except Convidados.DoesNotExist:
            messages.error(request, "Número de telefone não encontrado. Entre em contato com os papais do Téo para resolver esse problema" )

        #print(convidado)
        print(request.POST['telefone'])
        
    # return HttpResponse("Hello, world. You're at the polls index.")

    response = TemplateResponse(request, 'lista_presentes_app/index.html', {})
    return response

def obrigado(request):
    response = TemplateResponse(request, 'lista_presentes_app/obrigado.html', {})
    return response

@csrf_exempt
def logoff(request):
    if request.method == "POST":
        request.session['convidado'] = None
        request.session['user'] = None
        logout(request)
        return redirect('index')

def salvar_selecao(request):
    id_convidado = Convidados.objects.get(pk=request.session["convidado"]['id'])
    presentes_convidados = PresentesConvidados.objects.filter(id_convidado = id_convidado).delete()
    print(request.POST)
    # print(len(presentes_convidados))
    # presentes_convidados.delete()
    if request.POST["opcional"] != "":
        opcional = request.POST["opcional"]
        print({opcional})
        id_presente=Presentes.objects.get(pk=opcional)
        if len(PresentesConvidados.objects.filter(id_convidado=request.session["convidado"]['id'], id_presente=opcional)) == 0:
            PresentesConvidados.objects.create(
                id_convidado=Convidados.objects.get(pk=request.session["convidado"]['id']), 
                id_presente=id_presente, 
                quantidade=1)

    if request.POST["obrigatorio"] != "":
        obrigatorio = request.POST["obrigatorio"]
        print({obrigatorio})
        id_presente=Presentes.objects.get(pk=obrigatorio)
        if len(PresentesConvidados.objects.filter(id_convidado=request.session["convidado"]['id'], id_presente=obrigatorio)) == 0:
            PresentesConvidados.objects.create(
                id_convidado=Convidados.objects.get(pk=request.session["convidado"]['id']), 
                id_presente=id_presente, 
                quantidade=1)

    return JsonResponse({'ok':True})

class OpcoesView(generic.ListView):
    context_object_name = "data"
    template_name = "lista_presentes_app/opcoes.html"
    def get_queryset(self):        
        return {
            "obrigatorios": VwResultadosProdutos.objects.filter(obrigatorio=True,qtde_selecionada__lt=F('quantidade')).order_by('nome'),
            "opcionais": VwResultadosProdutos.objects.filter(obrigatorio=False,qtde_selecionada__lt=F('quantidade')).order_by('nome')
        }
        

class PresenteListView(generic.ListView):
    model = Presentes
    
class PresenteCreateView(generic.CreateView):
    model = Presentes
    fields = ('nome', 'quantidade', 'obrigatorio', 'url_imagem', 'url_anuncio')
    success_url = "/app/presentes"
    
class PresenteUpdateView(generic.UpdateView):
    model = Presentes
    slug_url_kwarg = 'presente_slug'
    slug_field = 'id'
    fields =('nome', 'quantidade', 'obrigatorio', 'url_imagem', 'url_anuncio')
    success_url = "/app/presentes"
    
    
class ConvidadoListView(generic.ListView):
    model = Convidados
    
class ConvidadoCreateView(generic.CreateView):
    model = Convidados
    fields = ('nome', 'email', 'telefone')
    success_url = "/app/convidados"
    
class ConvidadoUpdateView(generic.UpdateView):
    model = Convidados
    slug_url_kwarg = 'convidado_slug'
    slug_field = 'id'
    fields =('nome', 'email', 'telefone')
    success_url = "/app/convidados"
    
class ResultadoView(generic.ListView):
    context_object_name = "data"
    template_name = "lista_presentes_app/resultado.html"
    def get_queryset(self):
        return {
            "obrigatorios": VwResultadosProdutos.objects.filter(obrigatorio=True).order_by('-qtde_selecionada'),
            "opcionais": VwResultadosProdutos.objects.filter(obrigatorio=False).order_by('-qtde_selecionada')
        }


def login_user(request):
    request.session['convidado'] = None
    request.session['user'] = None
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/app')
            else:
                messages.error(request, "Usuário inválido" )
        else:
            messages.error(request, "Usuário/senha inválido(s)" )
    return TemplateResponse(request, 'lista_presentes_app/login.html', {})