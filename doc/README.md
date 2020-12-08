# Documentation

## Como aniadir un Floating Action Button (FAB)

Para esto usaremos el widget fab ya implementado. Dentro del html de la pagina en la que queramos aniadirlo aniadiremos el _include_:

```
    {% include 'widgets/fab.html'%}
```

Al ser fixed no importa el lugar, pero para mantener una estetica global, seria recomendable ponerlo al final del _block_. A continuacinon deberemos aniadir al _block_ de _css_ su clase asociada:

```
    <link rel="stylesheet" type="text/css" href="{% static 'css/widgets/fab.css' %}">  
```

Por ultimo, para aniadir funcionalidad lo haremos a traves de Vue, para ello, en el _block_ de _js_ aniadiremos el cnodigo correspondiente:

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