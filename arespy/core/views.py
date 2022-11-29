from django.shortcuts import render

# Create your views here.
from .models import leitePreco
from .serializers import leitePrecoSerializer
from .services import scrap_leite_cepea

from rest_framework import viewsets
#from rest_framework import permissions


class updateCepeaViewSet(viewsets.ModelViewSet):
    scrap_leite_cepea.Cepea.update_all_tables()

class reloadCepeaViewSet(viewsets.ModelViewSet):
    scrap_leite_cepea.Cepea.update_all_tables()

class leitePrecoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #print(scrap_leite_cepea.Cepea.df_leite)
    leitePreco.data = scrap_leite_cepea.Cepea.df_leite
    queryset = leitePreco.objects.all()
    serializer_class = leitePrecoSerializer
    serializer_class = scrap_leite_cepea.Cepea.df_leite
    #permission_classes = [permissions.IsAuthenticated]