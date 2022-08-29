from django.db import models

class Presentes(models.Model):
    nome = models.CharField(max_length=50)
    obrigatorio = models.BooleanField()
    quantidade = models.IntegerField()
    url_imagem = models.TextField(max_length=512, blank=True, null=True)
    url_anuncio = models.TextField(max_length=512, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'presentes'
        
class Convidados(models.Model):
    nome = models.CharField(max_length=50)
    email = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'convidados'

class PresentesConvidados(models.Model):
    id_convidado = models.ForeignKey(Convidados, models.DO_NOTHING, db_column='id_convidado', blank=True, null=True)
    id_presente = models.ForeignKey(Presentes, models.DO_NOTHING, db_column='id_presente', blank=True, null=True)
    quantidade = models.IntegerField(blank=True, null=True)    

    class Meta:
        managed = False
        db_table = 'presentes_convidados'


class VwResultadosProdutos(models.Model):
    nome = models.CharField(max_length=50)
    obrigatorio = models.BooleanField()
    quantidade = models.IntegerField()
    url_imagem = models.TextField(max_length=512, blank=True, null=True)
    url_anuncio = models.TextField(max_length=512, blank=True, null=True)
    qtde_convidados = models.IntegerField()
    qtde_selecionada = models.IntegerField()
    qtde_restante = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vw_resultado_produtos'