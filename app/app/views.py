# Create your views here.
from django.http import HttpResponseRedirect


def redirect_to_swagger(request):
    return HttpResponseRedirect(redirect_to='/swagger')
