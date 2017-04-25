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
saludo = 'Bienvenido al Acortador 2.0'
link = '<a ref='
link2='</a>'
# campo del formulario
campo = 'url='
# las urls deben empezar asi
prefix = 'http://'
index = 0 #Primera URL acortada, empieza en 0



"""
    Métodos auxiliares
    makeURL--> si la URL no empieza por http://, se lo añado
"""

def makeURL(URL, start):
    #Devuelve la URL con el prefijo añadido
    if not URL.startswith(start):
        URL = start + URL
    return URL
"""
 Métodos principales de views.py
"""
@csrf_exempt # esto se pone para que al hacer un POST no salten temas de seguridad
def Start (request):
    """
        Cuando se solicita el recurso http://.../acorta/
        Dependiendo del tipo de método, decide qué acción realizar
        Elabora la respuesta al cliente
    """
    # Si no lo pongo, python interpreta 'index' como variable local
    global index
    # Dirección en la que corre el servidor Django
    domain = request.get_host() #domain = localhost:8080
    #Metodo usado en la peticion
    metodo = request.method
    if metodo == 'GET':
        # Devolver el formulario junto a la lista de URLS acortadas hasta el momento
        list = URLModel.objects.all()   #Listado de todas las URLs del modelo
        template = loader.get_template('acorta/plantilla.html')
        context = {
            'intro': saludo,
            'second_line':'Ahora con Django!',
            'form': True,
            'show_list': True,
            'list_text':'Échale un vistazo a las URLs acortadas hasta el momento',
            'larga_list': URLModel.objects.all(),
        }
        # Mandamos la respuesta
        return HttpResponse(template.render(context, request))
    elif metodo == 'POST':
        # Cuerpo del POST
        body = request.body.decode('utf-8')
        # URL introducida en el formulario
        URL = body.split('=')[1] # Me quedo con la URL introducida en el formulario
        # Eliminamos los errores al decodificar (%20%23... cosas así)
        URL = urllib.parse.unquote(URL)
        # Si no empieza por http, se lo añadimos
        URL = makeURL(URL, prefix)
        if URL == prefix:
            # Si no hay qs, mando mensaje de error y enlace a la pagina original
            template = loader.get_template('acorta/plantilla.html')
            context = {
                'intro': '400 Bad Request',
                'second_line': 'Introduce una URL en el recuadrito, gracioso',
                'noURL_error': True,
                'noURL_error_message': 'Para volver a la página principal haz click ',
                'noURL_error_link': prefix+domain+'/acorta',
            }
            return HttpResponse(template.render(context, request))
        else:
            # Si hay URL, compruebo la base de datos y mando la url acortada
            context={
                'intro': 'Acortamiento realizado con éxito',
                'third_line': 'La url se encontraba en la base de datos',
            }
            template = loader.get_template('acorta/plantilla.html')
            try:
                URLCorta = URLModel.objects.get(larga=URL).corta
            except URLModel.DoesNotExist:
                # La url solicitada no está en la base de datos
                # localiza el siguiente índice libre
                index = URLModel.Search_Last_Index(URLModel, domain)
                #  Creamos la nueva url acortada
                URLCorta = prefix+ domain+'/acorta/'+str(index)
                # Guardamos la nueva entrada en la base de datos
                new = URLModel(larga= URL, corta = URLCorta)
                new.save()
                context.update({
                    'third_line': 'La url no estaba en la base de datos',
                })
            #elaboramos la respuesta
            context.update({
                'loop_message':'¿Qué mas quieres de mi?',
                'loop_message_option1':'Visitar url corta: ',
                'url_corta': URLCorta,
                'url_larga': URL,
                'loop_message_option2':'Visitar url larga: ',
                'back_message': 'Volver a la página principal. Pincha',
                'back_link': prefix+domain+'/acorta', #link a la página principal
                })

            return HttpResponse(template.render(context, request))
    else:
        return HttpResponse('<h1> Metodo invalido</h1>')

def NoMatch(request):
    #Si lo introducido no casa con ninguna url válida
    template = loader.get_template('acorta/plantilla.html')
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
    url_corta = prefix+domain+'/acorta/'+indice
    template = loader.get_template('acorta/petition.html')

    try:
        url_larga = URLModel.objects.get(corta=url_corta).larga
        respuesta = redireccion1 + str(url_larga)+ redireccion2
    except URLModel.DoesNotExist:
        context = {
            'intro': '404 Not Found',
            'second_msg': 'La url solicitada no se encuentra en la base de datos',
            'back_message': 'Para volver a la página principal haz click',
            'back_link': prefix+domain+'/acorta',
            'info': 'Visita la página y prueba a acortar alguna URL. Es gratis, agarrao',
        }
        return HttpResponse(template.render(context, request))
    return HttpResponse(respuesta)
