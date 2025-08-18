from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ActivityLog

class ActivityLogListView(LoginRequiredMixin, TemplateView):
    template_name = 'activity_logs/activity_log_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity_logs'] = ActivityLog.objects.select_related(
            'user', 'content_type'
        ).order_by('-timestamp')[:100]
        return context

class SecurityEventListView(LoginRequiredMixin, TemplateView):
    template_name = 'activity_logs/security.html'
