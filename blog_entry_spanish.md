# Métodos de importación de scripts.

Nivel conocimiento: Intermedio (Imports, ambientes, comandos)

Tiempo de lectura: 30 minutos

## Introducción

Puede que te hayas encontrado con esta situación: Se tiene un proyecto python que ha estado creciendo, después de una refactorización se han creado dos carpetas: una que conforma el paquete principal y otra de scripts que no es parte del paquete, pero depende de este. La estructura es la siguiente:

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

**Nota:** la línea **"`if __name__ == '__main__':`"**, a grandes rasgos, diferencia si el archivo es ejecutado directamente como script o importado por otro archivo como módulo, de esto depende si el contenido del `if` se ejecuta o no respectivamente. Puedes leer más detalles de esto en [este artículo](https://realpython.com/if-name-main-python/).

Dependiendo de cómo se intente acceder al archivo `script.py` este podría funcionar o no por una u otra razón. Los siguientes son métodos, basados en esta estructura, para lograr que los archivos en el directorio en `scripts` funcionen correctamente.

## Caso 1: El punto de ejecución importa

Basado en esta estructura es posible ejecutar cualquier script si se invoca como módulo, pero tiene que hacerse desde la ubicación correcta.

``` bash
\case1\project> python -m scripts.script
Welcome from foo!

\case1\project> python
>>> from scripts.script import main
>>> main()
Welcome from foo!
```

Esto funciona porque, por un lado, el punto de ejecución del intérprete es `\case1\project` y, por orto lado, la línea `from package.module import foo` del archivo `script.py` hace referencia al directorio `package` igualmente contenido en `\case1\project`. Para entender mejor el concepto de directorios de importación se puede leer [este artículo](https://www.howtouselinux.com/post/understanding-sys-path-in-python).

Por otro lado, cuando se ejecuta el archivo como script este no funciona:

``` bash
\case1\project> python scripts\script.py
ModuleNotFoundError: No module named 'package'
```

Lo que pasa aquí es que sin importar desde donde se invoque el archivo, mientras se invoque como script, el punto de ejecución del interprete es `\case1\project\scripts`. En ese directorio no existe `package` lo que genera la excepción `ModuleNotFoundError`.

Ejercicio: Agrega el siguiente archivo, intenta ejecutar el comando anterior y explica que el resultado.

``` python
# case1/project/scripts/package/module.py
def foo():
    return 'Welcome from distinct foo!'
```

### Ventajas:
- Es el más sencillo de los métodos en cuanto a que no necesita agregar código.

### Desventaja:
- Tiene que conocerse el directorio de ejecución del intérprete y que paquetes estan disponibles desde dicho directorio. La comprensión de importación de paquetes es necesaria.

- Si el script depende de dos paquetes contenidos en distintos directorios no funcionará este método.

### Recomendado
- Cuando las ejecuciones de scripts son la excepción, no la regla, y todos los paquetes en desarrollo están en el mismo directorio.

## Caso 2: Ampliar los directorios de importación

Para este caso el archivo `script.py` de caso 2.1 se ha modificado, el resto continúa igual.

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

Aquí, a grandes rasgos, la librería `os` da acceso a funcionalidades del sistema operativo, `sys` da acceso a variables que usa el intérprete de Python. `__file__` es la ruta absoluta de `script.py`, `currentdir` es el directorio de la carpeta `scripts` y `parentdir` el de `project`, este último directorio se agrega a `sys.path` que, si ya leeíste [el artículo](https://www.howtouselinux.com/post/understanding-sys-path-in-python), sabrás que este directorio también se inspeccionará al momento de buscar `package`, por esto el programa funciona sin importar la forma o el lugar donde se invoque el script.

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

Pero esto tiene un problema. Repetir la misma porción de código en todos los scripts es tardado y difícil de mantener. Una solución para esto es agregar un archivo de inicialización de scripts como en el caso 2.2:

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

Esto permite que en el script pueda ejecutarse desde cualquier ubicación, pero no se puede importar de otro lado que no sea la carpeta `scripts`.

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

Ejercicio: Explicar por qué la ejecución como script funciona desde cualquier punto, pero no la importación.

### Ventajas
- Con este método puedes incluir todos los directorios de todos los paquetes que estés desarrollando.

### Desventajas
- Tienes que elegir entre difícil de mantener (caso 2.1) y limitar desde donde se puede importar (caso 2.2).

### Recomendado
- Este método me ha funcionado en proyectos con notebooks, en caso de paquetes prefiero el método 3.

## Caso 3: Instalar el paquete

De entre todas formas de ejecutar los scripts en este post seguramente lo más sencillo sea instalar el paquete que se está elaborando. En este caso se utilizará la librería integrada de `setuptools`.

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

También recomiendo crear y activar un entorno virtual para no modificar la versión de Python que se tiene instalada (entiende más de entornos virtuales en [este artículo](https://realpython.com/python-virtual-environments-a-primer/)). Posteriormente, se instala el paquete.

``` bash
\case3\project> python -m venv venv
\case3\project> .\venv\scripts\activate
(venv) \case3\project\ python setup.py install
```

Ahora es posible usar los scripts desde cualquier lugar invocados de cualquier manera.

``` bash
\case3> python project\scripts\script.py
Welcome from foo!

\case3> python
>>> from project.scripts.script import main
>>> main()
Welcome from foo!

\case3> python -m project.scripts.script
Welcome from foo!

\case3\project\script> python -m script
Welcome from foo!
```

### Ventajas
- Es el método más limpio y fácil de implementar que permite a los archivos funcionar desde cualquier ubicación o forma de invocación

### Desventaja
- Se recomienda encarecidamente usar un ambiente virtual para no ensuciar la instalación de Python.
- Se tiene que reinstalar el paquete cada vez que el mismo tenga un cambio.
- La instalación generará directorios que muy probablemente no se quieren versionar, puedes ver que carpetas se excluyen del versionado en el `.gitignore` de este proyecto.

### Recomendado
- En general es el método recomendado para cualquier caso.

## Caso 4: Punto de entrada

Este método lo considero el más difícil de todos por lo mucho que puede aumentar la lógica y complejidad de un proyecto. La idea es agregar un archivo que va a funcionar como punto de entrada, si has trabajado con Django te sonará el archivo `manage.py`, archivo que funciona como punto de entrada para las funcionalidades principales de los proyectos. En este caso se agrega la versión más simple que se me ha ocurrido de un punto único de entrada.

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

Aquí la función `dispatch` se encarga de determinar que acción realizar dependiendo de los argumentos de la ejecución. La función `run_script` se encarga de ejecutar el script. Nota que este script hace varios supuestos como dos argumentos por ejecución o que todos los scripts tendrán una función `main`, parecido al método `handle` en las [clases para comandos](https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/) en Django. Otra cosa a notar es que este script únicamente se puede invocar desde el directorio del proyecto.

``` bash
\case4\project> python run.py script script
Welcome from foo!

\case4\project> python run.py script another_script
Exception: Unknown script "another_script"

\case4\project> python run.py script
Exception: Must have 2 parameters

\case4\project> python run.py test general_test
Exception: Unknown command
```

Otras aproximaciones de este método mueven la carpeta de `scripts` dentro de `paquete` (algo más parecido a los `commands` de Django).

### Ventajas
- Siempre es más seguro tener un único punto de entrada multipropósito que tener múltiples puntos de entrada individuales.
- El **punto de entrada único** en sí mismo es una forma de documentar el proyecto.

### Desventajas
- En necesaria una implementación de la lógica en el punto de entrada, su complejidad dependerá de las características que se deseen agregar al proyecto.

### Recomendado
- Para proyectos de gran tamaño (tómese de ejemplo Django), en librerías pensadas en usarse desde consola o, por supuesto, cuando se desea tener un punto de entrada único a la aplicación.

## Conclusión
A menos que exista un requerimiento que dicte lo contrario, yo recomendaría hacer uso del caso 3 para ejecutar scripts o tests constantemente y el caso 1 cuando la ejecución de scripts sea más una excepción que una regla, sin olvidar posicionarse en la carpeta adecuada.

## REFERENCIAS
- [(Stack Overflow) How to properly structure internal scripts in a Python project?](https://stackoverflow.com/questions/57744466/how-to-properly-structure-internal-scripts-in-a-python-project)
- [understanding sys.path in Python](https://www.howtouselinux.com/post/understanding-sys-path-in-python)
- [What Does if \_\_name__ == "\_\_main__" Do in Python?](https://realpython.com/if-name-main-python/)
- [A Practical Guide to Using Setup.py](https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/)
- [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)
- [How to create custom django-admin commands](https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/)