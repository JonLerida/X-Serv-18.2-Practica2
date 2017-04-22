from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site
# Create your views here.

formulario = "<form method= POST> Escribe tu URL: <input type='text' name='url'>"
formulario += "<input type=submit value='Pulsame, por Dios' style='height:50px; width:125px'></form> "

redireccion1 = ("<!DOCTYPE html>\r\n<html>\r\n<head>\r\n"+
                    "<meta http-equiv='Refresh' content='1;url=")
redireccion2 = "'><body><h2>Redireccionandote...no te muevas!</h></body></html>"
saludo = '<h1> Bienvenido al Acortador2.0</h1><h2>Ahora con Django!</h2>'
link = '<a ref='
link2='</a>'
# campo del formulario
campo = 'url='
# las urls deben empezar asi
prefix = 'http://'

index = 0 #Primera URL acortada, empieza en 0
@csrf_exempt # esto se pone para que al hacer un POST no salten temas de seguridad
def Start (request):
    # Dirección en la que corre el servidor Django
    domain = request.get_host() #domain = localhost:8080
    #Metodo usado en la peticion
    metodo = request.method
    if metodo == 'GET':
        # Devolver el formulario junto a la lista de URLS acortadas hasta el momento
        respuesta = saludo+formulario
        respuesta += 'aqui van todas las URLS acortadas...'
        return HttpResponse(respuesta)
    elif metodo == 'POST':
        # Cuerpo del POST
        body = request.body.decode('utf-8')
        # URL introducida en el formulario
        URL = body.split('=')[1] # Me quedo con la URL introducida en el formulario
        if URL == '':
            # Si no hay qs, mando mensaje de error y enlace a la pagina original
            respuesta = '<h1>400 Bad Request</h1>'
            respuesta += '<h2>Introduce una URL en el recuadrito, gracioso</h2>'
            respuesta += "<p>Para volver a la página principal haz click <a href="+prefix+domain+'/acorta'+">aquí</a></p>"
            return HttpResponse(respuesta)
        else:
            # Si hay URL, compruebo si la tengo guardada ya y elaboro la respesta
            respuesta = '<h1>Dirección acortada con éxito</h1>'
            respuesta += '<h2>url introducida: '+URL+'</h2>'
            return HttpResponse(respuesta)

def NoMatch(request):
    return HttpResponse('<h1>Introduce algo útil, bro</h1>')

def Petition(request, url_corta):
    return HttpResponse('<h1>Comprobando la URL en la base de datos...</h1>' + url_corta)
