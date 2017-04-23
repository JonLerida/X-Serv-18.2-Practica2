from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site
from .models import URLModel
import urllib
from django.template import loader
# Create your views here.

formulario = "<form method= POST> Escribe tu URL: <input type='text' name='url'>"
formulario += "<input type=submit value='Púlsame, por Dios' style='height:50px; width:125px'></form> "


redireccion1 = ("<!DOCTYPE html>\r\n<html>\r\n<head>\r\n"+
                    "<meta http-equiv='Refresh' content='0;url=")
redireccion2 = "'><body><h2>Redireccionandote...no te muevas!</h></body></html>"
saludo = 'Bienvenido al Acortador2.0'
link = '<a ref='
link2='</a>'
# campo del formulario
campo = 'url='
# las urls deben empezar asi
prefix = 'http://'
index = 0 #Primera URL acortada, empieza en 0



""" Métodos auxiliares
    makeURL--> si la URL no empieza por http://, se lo añadiendo
"""

def makeURL(URL, start):
    #Devuelve la URL con el prefijo añadido
    if not URL.startswith(start):
        URL = start + URL
    return URL
""" Métodos principales de views.py
"""
@csrf_exempt # esto se pone para que al hacer un POST no salten temas de seguridad
def Start (request):
    global index
    """
        Cuando se solicita el recurso http://.../acorta/
        Dependiendo del tipo de método, decide qué acción realizar
        Elabora la respuesta al cliente
    """
    # Dirección en la que corre el servidor Django
    domain = request.get_host() #domain = localhost:8080
    #Metodo usado en la peticion
    metodo = request.method
    print(request.body)
    if metodo == 'GET':
        # Devolver el formulario junto a la lista de URLS acortadas hasta el momento
        respuesta = saludo+formulario
        respuesta += '<h2>Base de datos actual:</h2><ul>'
        list = URLModel.objects.all()
        template = loader.get_template('acorta/prueba.html')
        context = {
            'intro': saludo,
            'second_line':'Ahora con Django!',
            'form': True,
            'show_list': True,
            'list_text':'Échale un vistazo a las URLs acortadas hasta el momento',
            'larga_list': URLModel.objects.all(),
        }
        return HttpResponse(template.render(context, request))
        for element in list:
            larga = element.larga
            corta = element.corta
            respuesta += '<li>URL larga: ' + larga +' | URL corta: '+corta+'</li>'
        respuesta += '</ul>'
        return HttpResponse(respuesta)
    elif metodo == 'POST':
        # Cuerpo del POST
        body = request.body.decode('utf-8')
        # URL introducida en el formulario
        URL = body.split('=')[1] # Me quedo con la URL introducida en el formulario
        # Eliminamos los errores al decodificar (urllib.parse.unquote)
        URL = urllib.parse.unquote(URL)
        # Si no empieza por http, se lo añadimos
        URL = makeURL(URL, prefix)
        print('URL solicitada: '+URL)

        if URL == prefix:
            # Si no hay qs, mando mensaje de error y enlace a la pagina original
            respuesta = '<h1>400 Bad Request</h1>'
            respuesta += '<h2>Introduce una URL en el recuadrito, gracioso</h2>'
            respuesta += "<p>Para volver a la página principal haz click <a href="+prefix+domain+'/acorta'+">aquí</a></p>"
            return HttpResponse(respuesta)
        else:
            # Si hay URL, compruebo si la tengo guardada ya y elaboro la respesta
            try:
                URLCorta = URLModel.objects.get(larga=URL).corta
                print(URLCorta)
                respuesta = '<h1>Acortamiento realizado con éxito</h1>'
                respuesta +='<h2>La url se encontraba en la base de datos</h2>'
            except URLModel.DoesNotExist:
                print('Recurso no existente en la base de datos. Añadiendo')
                #Localiza el siguiente índice de URL corta
                index = URLModel.Search_Last_Index(URLModel, domain)
                URLCorta = prefix+ domain+'/acorta/'+str(index)
                print(URLCorta)
                print(URL)
                new = URLModel(larga= URL, corta = URLCorta)
                new.save()
                respuesta = '<h1>Acortamiento realizado con éxito</h1>'
                respuesta += '<h2>La url recibida no estaba en la base de datos</h2>'

            respuesta += "<p>¿Qué más quieres de mi?</p>\r\n<ul>"
            respuesta += "<li>Visitar url corta: <a href='%s'>%s</a></li>\r\n"
            respuesta += "<li>Visitar url larga: <a href='%s'>%s</a></li>\r\n"
            respuesta +="<li>Volver a la página principal. Pincha <a href='%s'>%s</a></li>\r\n</ul>"

            return HttpResponse(respuesta %(URLCorta, URLCorta, str(URL), str(URL), prefix+domain+'/acorta', 'aqui.'))

def NoMatch(request):
    template = loader.get_template('acorta/prueba.html')
    context = {
        'intro': 'Lamentablemente el recurso solicitado no está disponible',
        'list_text':'Sin embargo, no todo son malas noticias. Aquí tienes una lista de las URLs que han sido acortadas hasta la fecha',
        'larga_list': URLModel.objects.all(),
        'show_list': True,
    }
    return HttpResponse(template.render(context, request))

def Petition(request, indice):
    global prefix, redireccion1, redireccion2
    domain = request.get_host() #domain = localhost:8080
    try:
        url_corta = prefix+domain+'/acorta/'+indice
        print(url_corta)
        url_larga = URLModel.objects.get(corta=url_corta).larga
        print(url_larga)
        respuesta = redireccion1 + str(url_larga)+ redireccion2
    except URLModel.DoesNotExist:
        respuesta = '<h1> 404 Not Found</h1>'
        respuesta += '<h2> :$ no tenemos el recurso que pides...</h2>'
        respuesta += "<p>Para volver a la página principal haz click <a href="+prefix+domain+'/acorta'+">aquí</a></p>"
    return HttpResponse(respuesta)
