from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from smehs.models import Smeh
# Create your views here.
class ShowSmehsView(TemplateView):
    template_name="smehs/show_smehs.html"
    
    def get_context_data(self,**kwargs:Any)->dict[str,Any]:
        context = super().get_context_data(**kwargs)
        context['smehs']=Smeh.objects.all()
        
        return context
#    def get(request,*args,**kwargs):
#     smehs=Smeh.objects.all()

#     result=""
#     for s in smehs:
#         result+=s.name+"<br>"
#     return HttpResponse(result)