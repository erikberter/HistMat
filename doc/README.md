# Documentation

## Como aniadir un Floating Action Button (FAB)

Para esto usaremos el widget fab ya implementado. Dentro del html de la pagina en la que queramos añadirlo aniadiremos el _include_:

```
    {% include 'widgets/fab.html'%}
```

Al ser fixed no importa el lugar, pero para mantener una estetica global, seria recomendable ponerlo en el _block widgets_. A continuacinon deberemos añadir al _block_ de _css_ su clase asociada:

```
    <link rel="stylesheet" type="text/css" href="{% static 'css/widgets/fab.css' %}">  
```

Por ultimo, para añadir funcionalidad lo haremos a traves de Vue, para ello, en el _block_ de _js_ aniadiremos el cnodigo correspondiente:

```
    <script>
        var fab = new Vue({
            el: '#fab-container',
            data: {
                //Data
            },
            methods: {
                fab_action: function (event) {
                    //Action
                }
            }
        })
    </script>
```

Este codigo se compone de una inicializacinon de un Vue sobre el elemento fab. Dentro del mismo, hemos definido un _v-on:click="fab_action"_, que nos dice que al hacer click en el div ejecutara el metodo fab_action.

## Como aniadir un Toast 


Para esto usaremos el widget toast ya implementado. Dentro del html de la pagina en la que queramos añadirlo aniadiremos el _include_:

```
    {% include 'widgets/toast.html'%}
```


Al ser fixed no importa el lugar, pero para mantener una estetica global, seria recomendable ponerlo en el _block widgets_.  El CSS del toast es puramente de Bootstrap, por lo que no será necesario añadir una hoja de estilos.

Para usar poder usar el toast habrá que añadir su archivo _js_:

```
    <script src="{% static 'js/widgets/toast.js'%}"></script>
```

Una vez hecho, podremos ejecutar el toast mediante una sola llamada

```
    load_toast("Toast text");
```

### Traducción del mensaje

Para evitar la inconsistencia entre el lenguaje de la página y el del toast, es aconsejable utilizar un diccionario con los diferentes mensajes posibles

```
    TOAST_RESPONSE = {
        'book_page_change' : {
            'es' : 'Se ha cambiado la pagina correctamente',
            'en' : 'Page was correctly changed',
            'eu' : 'Pagina ondo aldatu da?'
        },
    }
```

junto con

```
    var toast_text = translate_text(TOAST_RESPONSE['book_page_change']);
    load_toast(toast_text);
```
