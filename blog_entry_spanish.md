# ImportError: attempted relative import with no known parent package. Estrategias de importación.

Nivel conocimiento: Intermedio (Imports, ambientes, comandos)
Tiempo de lectura: 30 minutos

## Introducción

Esta semana me he encontrado con una situación usual al desarrollar en Python y quiero aprovechar para compartir distintas estrategias para resolverla:

Se tiene un proyecto basado en python con una porción de código que funciona como la aplicación y otra porción de código que será el cliente (de dicha aplicación). Inicialmente ambas porciones de código estaban contenidas en el mismo archivo pero el proyecto he crecido, es hora de tomarlo en serio y el siguiente paso es refactorizar. Dependiendo de la lógica del proyecto y el como se dedecida refactorizar puede que hayan sudedido una de los siguientes 4 casos:

## Casos a analizar

### Caso 1: Archivos hermanados

```
.
└── src/
    ├── app.py
    └── client.py
```

Es muy usual que los proyectos desde cero en Python llegados a algún punto tenga este aspecto, por ejemplo, donde el cliente sea el programa principal y la aplicación sean los util, funciones recurrentes o una abstracción de clase; otro caso común es que el cliente sean scripts o tests y que aplicación sea el programa principal.

### Caso 2: Punto de entrada unico

``` 
.
└── src/
    ├── apps/
    │   └── app.py
    └── client.py
```
Este caso es un ejemplo de una entrada unica para una aplicación pueden ser archivos del tipo run.py o main.py que acceden a todas las funcionalidades de la app; el archivo manage.py de django trabaja con este concepto.

### Caso 3: Subdirectorio clientes

``` 
.
└── src/
    ├── clients/
    │   └── client.py
    └── app.py
```
Sin temor a equivocarme diré que esta es la menos común las formas de estructurar archivos en un proyecto python. El próximo caso es una version más general de la anterior y las estrategias de solución aplican practicamente igual.

### Caso 4: Subdirectorios hermanos

``` 
.
└── src/
    ├── apps/
    │   └── app.py
    └── clients/
        └── client.py
```
Este caso es muy común cuando se trabajan en proyectos grandes. El par aplicación y cliente pueden corresponder a un paquete con sus scripts o/y tests; incluso podría ser que la aplicación sean los scripts y el cliente los tests. Tal vez hayas visto esta estructura en proyectos que incluyan notebooks y seguramente las has visto cuando aplicación y cliente corresponden a subpaquetes de un paquete padre. Este será el principal caso a tener en cuenta en las estrategias de solución.

## Estrategias de importación

### Caso 1.1: Cliente en consola

En este caso los archivos hermanados son `script.py` y `app.py`, el primero consume al segundo, ambos contenidos en `src/`. La idea es invocar directamente a `script.py` desde distintos directorios y ver como se comporta.

``` python
### Estructura ###
# case11/
# └── src/
#     ├── app.py
#     └── script.py

# src/app.py
def foo():
    return 'Welcome from App foo!'

# src/script.py
import app

def main():
    print(app.foo())

if __name__ == '__main__':
    main()
```

**Nota:** la linea **`if __name__ == '__main__':`**, a muy grandes rasgos, diferencía si el archivo es ejecutado como script o importado como módulo, de esto depende si el contenido del `if` se ejecuta o no respectivamente. Puedes leer más detalles de esto en [este artículo](https://realpython.com/if-name-main-python/).

``` bash
\case11\src> python script.py
Welcome from App foo!

\case11> python src\script.py
Welcome from App foo!
```

Supongamos que la lógica cambia y ahora el script debe ejecutare desde el interprete entonces tiene que importarse, aqui el comportamiento del modulo será distinto dependiendo del directorio donde este posicionado el interprete.

``` bash
\case11\src> python
>>> import script
>>> script.main()
Welcome from App foo!

\case11> python
>>> from src import script
ModuleNotFoundError: No module named 'app'
```

===== Subencarpetar los clients:
Si el problema es que los clients no son parte del paquete, ¿Porqué no incluirlos en este? La idea es convertir a clients en un subpaquete y hacer el un import absoluto del contenido del paquete.
• recomendado para proyectos pequeños y medianos o donde no importa tener toda la logica en la mima subraiz
• No se recomienda si se quiere usar este metodo para dos paquetes sobre raiz
• El mas sencillo de todos
• Mantiene la logica mal estructurada
• Los clients no pueden invocarse desde cualquier lugar?
     • depende si se hacen relativos o absolutos 

===== a travez del path:
-> importando sys y direccionando a la posicion del paquete
• es el que menor requerimientos de conocimientos en python requiere
• no recomendado en trabajos serios
• No esta estilizado

===== Instalar el paquete:
-> Maneras de instalar un paquete
• recomendado para: proyectos medianos
• se puede instalar en un entorno aislado o en el sistema (se recomienda instalar en un ambiente)
• los imports relativos dejan de ser necesarios
• hay que saber instalar paquetes

===== crear un archivo como punto de entrada
• recomendado para: proyectos complejos
• elegante
• puedes aprovechar para incluirlo entre las formas de usar el paquete
• hay que programar toda la logia del punto de entrada
    • con un run.py
    • usando la libreria setuptools

===========
• Buscar y hacer funcionar mas methodos

# REFERENCIAS
https://www.datasciencelearner.com/importerror-attempted-relative-import-parent-package/

# TODO: Organizar