from django import http
from django.views import generic
from django.views.decorators.csrf import csrf_exempt


class ResponseView(generic.View):

    http_method_names = [u'post']

    def post(self, request, *args, **kwargs):
        print "request.POST : " + str(request.POST)
        return http.HttpResponse()

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        super(ResponseView, self).dispatch(request, *args, **kwargs)
