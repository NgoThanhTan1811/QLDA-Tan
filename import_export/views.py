from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DocumentListView(LoginRequiredMixin, TemplateView):
    template_name = 'import_export/documents.html'

class CustomsListView(LoginRequiredMixin, TemplateView):
    template_name = 'import_export/customs.html'
