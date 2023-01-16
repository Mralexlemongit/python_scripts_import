# ImportError: attempted relative import with no known parent package. Estrategías para importar carpetas.

Nivel conocimiento: Intermedio (Imports, ambientes, comandos)
Tiempo de lectura: 30 minutos

## Introducción

Esta semana me he encontrado con una situación usual que puede que te haya ocurrido y quise aprovechar para compartir estrategias dependiendo del tipo de desarrollo que estes llevando a cabo.

Se tiene un proyecto python que ha estado creciendo, despues de una refactorización se han creado dos carpetas: una carpeta que conforma el paquete principal y otra de scripts que no es parte del paquete pero depende de este. La estructura es la siguiente:

``` python
# .
# └── project/
#     ├── package/
#     │   └── module.py
#     └── scripts/
#         └── script.py

# ./project/package/module.py
def foo():
    return 'Welcome from foo!'

# ./project/scripts/script.py
from package.module import foo

def main():
    print(foo())

if __name__ == '__main__':
    main()
```

**Nota:** la linea **`if __name__ == '__main__':`**, a muy grandes rasgos, diferencía si el archivo es ejecutado directamente como script o importado por otro archivo como módulo, de esto depende si el contenido del `if` se ejecuta o no respectivamente. Puedes leer más detalles de esto en [este artículo](https://realpython.com/if-name-main-python/).

Dependiendo de como se intente acceder al archivo `script.py` este podría funcionar o no por una u otra razón. Las siguientes son estrategias basadas en esta estructura para lograr que los archivos contenidos en scripts funcionen correctamente.

## Caso 1: El punto de ejecución importa

Basado en la esta estrucutra es posible ejecutar cualquier script si se invoca como modulo pero tiene que hacerse desde la ubicación correcta, por ejemplo.

``` bash
\case1\project> python -m scripts.script
Welcome from foo!

\case1\project> python
>>> from scripts.script import main
>>> main()
Welcome from foo!
```

Esto funciona porque el punto de ejecución del interprete es `\case1\project`, en este directorio esta `package` que hace referencia a la linea `from package.module import foo` del archivo `script.py`. Para entender mejor el concepto de directorios de inportación puedes ayudarte leyendo [este artículo](https://www.howtouselinux.com/post/understanding-sys-path-in-python).

Ahora se invoca el archivo como script:

``` bash
\case1\project> python scripts\script.py
ModuleNotFoundError: No module named 'package'
```

En este caso, sin importar desde donde se invoque el archivo como script, el punto de ejecución es `\case1\project\scripts`. En este directorio no existe `package` por lo que no puede importarlo.

Ejercicio: Agrega el siguiente archivo, intenta ejecutar el comando anterior y explica que es lo que ha pasado.

``` python
# case1/project/scripts/package/module.py
def foo():
    return 'Welcome from distinct foo!'
```

### Ventajas:
- Es el más sencillo de los métodos.

### Desventaja:
- Tiene que conocerse el punto de arranque del interprete y la disposición de los paquetes desde ese punto. Es necesario cierta comprensión de los directorios de busqueda de paquetes.

- No hay manera de hacer esto (sin agregar código) si el script depende de dos paquetes contenidos en distintos directorios.

### Recomendado
- Cuando las ejecuciónes de scripts son practicamente nulas y todos los paqutes generados estan en el mismo directorio.

## Caso 2: Agregar el directorio del paquete

Para este caso el archivo `script.py` de caso 2.1 se ha modificado, el resto continua igual.

``` python
# case2.1/project/scripts/script.py
import os, sys

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from package.module import foo

def main():
    print(foo())

if __name__ == '__main__':
    main()
```

Aquí, a grandes rasgoz, la librería `os` da acceso a funcionalidades del sistema operativo, `sys` da acceso a variables que usa el interprete de Python. `__file__` es la ruta absoluta de `script.py`, `currentdir` es el directorio de la carpeta `scripts` y `parentdir` el de `project`, este último directorio se agrega a `sys.path` que, si ya leeiste [el articulo](https://www.howtouselinux.com/post/understanding-sys-path-in-python), sabras que este directorio tambien se inspeccionará al momento de buscar `package`, por esto el programa funciona sin importar la forma o el lugar donde se invoca el script.

``` bash
\case2.1> python project\scripts\script.py
Welcome from foo!

\case2.1> python
>>> from project.scripts.script import main
>>> main()
Welcome from foo!

\case2.1> python -m project.scripts.script
Welcome from foo!

\case2.1\project\script> python -m script
Welcome from foo!
```

Pero esto tiene un problema. Repetir la misma porción de código en todos los scripts es tardado y díficil de mantener. Una solución para esto es agregar un archivo de inicialización de scripts como en el caso 2.2:

``` python
# case2.2/project/scripts/initialization.py
import os, sys

print('Initialization scripts')

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# case2.2/project/scripts/script.py
import initialization

from package.module import foo

def main():
    print(foo())

if __name__ == '__main__':
    main()
```

Esto permite que en el script pueda ejecutarse desde cualquier ubicación pero no se puede importar de otro lado que no sea la carpeta `scripts`.

``` bash
\case2.2> python project\scripts\script.py
Scripts initialization
Welcome from foo!

\case2.2> python
>>> from project.scripts.script import main
ModuleNotFoundError: No module named 'initialization'

\case2.2> python -m project.scripts.script
ModuleNotFoundError: No module named 'initialization'

\case2.2\project\script> python -m script
Scripts initialization
Welcome from foo!
```

Ejercicio: Explicar porque la ejecución como script funciona desde cualquier punto pero no la importación.

### Ventajas
- Con este metodo puedes incluir todos los directorios de todos los paquetes que estes desarrollando.

### Desventajas
- Tienes que elegir entre difícil de mantener (caso 2.1) y limitar desde donde se puede importar (caso 2.2).

### Recomendado
- Este método me ha funcionado en proyectos con notebooks, en caso de paquetes prefiero el método 3.

## Caso 3: Instalar el paquete

De entre todas las estrategías incluidas en este post seguramente lo más sencillo sea instalar el paquete que se esta elavorando. En este caso se utilizara la librería integrada de `setuptools`.

``` python
# case3/project/setup.py
import setuptools

setuptools.setup(
    name="package",
    version="1.0.0",
    author="You",
    author_email="you@example.com",
    description="This is my project",
    packages=["package"],
)
```

Para entender este paquete y saber que más puedes hacer con él puedes leer [este artículo](https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/).

Antes que nada se recomienda crear y activar un entorno virtual para no modificar la version de python que se tiene instalada (entiende más de entornos virtuales en [este artículo](https://realpython.com/python-virtual-environments-a-primer/)). Posteriormente se instala el paquete.

``` bash
\case3\project> python -m venv venv
\case3\project> .\venv\scripts\activate
(venv) \case3\project\ python setup.py install
```

Ahora es posible usar los scripts desde cualquier lugar invocados de cualquier manera.

``` bash
\case2.2> python project\scripts\script.py
Welcome from foo!

\case2.2> python
>>> from project.scripts.script import main
>>> main()
Welcome from foo!

\case2.2> python -m project.scripts.script
Welcome from foo!

\case2.2\project\script> python -m script
Welcome from foo!
```

### Ventajas
- Es la estrategia mas limpia y fácil de implementar que permite a los archivos funcionar desde cualquier ubicación o forma de invocación

### Desventaja
- Se recomienda encarecidamente usar un ambiente virtual para no ensuciar la instalación de Python.
- Se tiene que reinstalar el paquete cada vez que tenga un cambio.
- La instalación generará directorios que muy probablemente no se quieren versionar, el ejemplo lo puedes ver en el `.gitignore` de este proyecto.

### Recomendado
- En general es el metodo recomendado para cualquier caso.

Caso 4: Punto de entrada

Esta estrategia la considero la más compleja de todas por lo mucho que puede aumentar la logica de un proyecto. La idea es agregar un archivo que va a funcionar como punto de entrada, si has trabajado con Django te sonará el archivo `manage.py` archivo que funciona como punto de entrada para las funcionalidades principales de los proyectos, en este caso se agregara la version más simple que se me puede ocurrir.

``` python
# case4/project/run.py
import sys

def dispatch(arguments=None):
    if arguments is None or len(arguments) != 2:
        raise Exception('Must have 2 parameters')
    
    if arguments[0] == 'script':
        run_script(arguments[1])
    else:
        raise Exception('Unknown command')

def run_script(name):
    try:
        exec(f'from scripts import {name}')
    except ImportError:
        raise Exception(f'Unknown script "{name}"')
        
    exec(f'{name}.main()')

if __name__ == '__main__':
    dispatch(sys.argv[1:])
```

Aquí la función `dispatch` se encarga de determinar que acción realizar dependiendo de los argumentos de la ejecución. La función `run_script` se encarga de ejecutar el script. Nota que este script hace varios supuestos como dos argumentos por ejecución o que todos los scripts tendran una función `main`, parecido al método `handle` en las clases para comandos en django. Este escript unicamente se puede invocar desde el directorio del projecto.

``` bash
\case4\project> python run.py script script
Welcome from foo!

\case4\project> python run.py script another_script
Exception: Uknow script "another_script"
```


REFERENCIAS
https://www.datasciencelearner.com/importerror-attempted-relative-import-parent-package/
https://careerkarma.com/blog/python-beyond-top-level-package-error-in-relative-import/
https://stackoverflow.com/questions/57744466/how-to-properly-structure-internal-scripts-in-a-python-project
https://www.howtouselinux.com/post/understanding-sys-path-in-python
https://realpython.com/if-name-main-python/
https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
https://realpython.com/python-virtual-environments-a-primer/

CASO 3: Instalar el paquete en un entorno virtual


CASO 4: Crear un punto de entrada
- En necesario una implementación de la logica dentro del archivo de punto de entrada, esto requiere cierto nivel de conocimiento del lenguage
- esta logica es comun en proyectos grandes (tomese de ejemplo django), en librerias pensadas en usarse desde consola o, por supuesto, cuando se desea tener un punto de entrada unico a la aplicación.
- cave destacar que hay distintas estrategias y librerias para implementar el archivo run.py por lo que la complejidad de esta puede aumentar significativamente

En resumen, a menos que sea requerido algo en particular yo te recomendaria hacer uso del caso 3 si es planeas correr scripts o tests contantemente y el caso 1 si solo necesitas correr un escript referenciando a un paquete pocas veces sin olvidar posicionarte en la carpeta adecuada.