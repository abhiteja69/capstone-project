from django.shortcuts import render
from . forms import DiaryForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from . models import Diaryt

from django.views.generic import CreateView, FormView, ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from . serializers import DiarytSerializer
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


class Registerdiaryt(SuccessMessageMixin, CreateView):
    form_class = DiaryForm
    template_name = 'diaryts/new_diaryt.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        #form.instance.seen_by = None
        form.save()

        messages.success(self.request,
                         'Your diary was registered successfully.')

        return HttpResponseRedirect(reverse('accounts:dashboard'))


class Listdiaryts(ListView):
    model = Diaryt
    template_name = 'diaryts/all_diaryts.html'


class Detaildiaryts(DetailView):
    model = Diaryt
    template_name = 'diaryts/diaryts_detail.html'

   



class DiarytView(viewsets.ModelViewSet):
    Diaryt = get_user_model()
    queryset = Diaryt.objects.all()
    serializer_class = DiarytSerializer

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        return Response("ok")


class DiarytList(generics.ListAPIView):
    serializer_class = DiarytSerializer


    def get_queryset(self):
        user = self.request.user
       
        return Diaryt.objects.filter(created_by=user)
