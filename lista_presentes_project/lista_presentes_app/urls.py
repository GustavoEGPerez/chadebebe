from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('opcoes/', views.OpcoesView.as_view(), name='opcoes'),
    path('resultado/', views.ResultadoView.as_view(), name='resultado'),
    path('presentes/', views.PresenteListView.as_view(), name='presentes'),
    path('presentes/<slug:presente_slug>/', views.PresenteUpdateView.as_view(),name='presentes_edit'),
    path('presentes/new', views.PresenteCreateView.as_view(), name='presentes_new'),
    path('convidados/', views.ConvidadoListView.as_view(), name='convidados'),
    path('convidados/<slug:convidado_slug>/', views.ConvidadoUpdateView.as_view(),name='convidados_edit'),
    path('convidados/new', views.ConvidadoCreateView.as_view(), name='convidados_new'),
    path('logoff', views.logoff, name='convidados_new'),
    path('save_selection', views.salvar_selecao, name='salvar_selecao'),
    path('obrigado', views.obrigado, name='obrigado'),
    path('convite', views.convite, name='convite')
]