# Documentation

## Como añadir un Floating Action Button (FAB)

Para esto usaremos el widget fab ya implementado. Dentro del html de la página en la que queramos añadirlo añadiremos el _include_:

```
    {% include 'widgets/fab.html'%}
```

Al ser fixed no importa el lugar, pero para mantener una estetica global, seria recomendable ponerlo al final del _block_. A continuación deberemos añadir al _block_ de _css_ su clase asociada:

```
    <link rel="stylesheet" type="text/css" href="{% static 'css/widgets/fab.css' %}">  
```

Por último, para añadir funcionalidad lo haremos a través de Vue, para ello, en el _block_ de _js_ añadiremos el código correspondiente:

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

Este codigo se compone de una inicialización de un Vue sobre el elemento fab. Dentro del mismo, hemos definido un _v-on:click="fab_action"_, que nos dice que al hacer click en el div ejecutará el método fab_action.