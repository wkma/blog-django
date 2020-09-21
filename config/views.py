from django.http import HttpResponse
from django.views.generic import ListView

from theblog.views import CommonViewMixin
from .models import Link

class LinkListView(CommonViewMixin,ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'
def inde(request):
    x ="<h1>宇宙之大，马车之小</h1>"
    return HttpResponse(x)
# def links(request):
#     return HttpResponse("links")