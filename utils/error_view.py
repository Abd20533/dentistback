from django.http import JsonResponse


def handler404(request,exception):
     message=('path not found')
     response=JsonResponse(data={'error':message})
     response.status_code=404
     return response


def handler400(request,exception):
     message=('error __400__ ')
     response=JsonResponse(data={'error':message})
     response.status_code=400
     return response
 
 
def handler500(request):
     message=(' internal server error')
     response=JsonResponse(data={'error':message})
     response.status_code=500
     return response