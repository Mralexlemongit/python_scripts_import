# ImportError: attempted relative import with no known parent package. Estrategias de importación.

Nivel conocimiento: Python intermedio (Imports, ambientes, comandos)
Tiempo de lectura: 30 minutos

## Introducción

Esta semana me he encontrado con un problema típico al desarrollar Python y quiero aprovechar para compartir distintas estrategias para solucionarlo:

Se tiene un proyecto basado en python con una porsion de código que funciona como la aplicación y otra porsion de código que será el  cliente (de dicha aplicación). Inicialmente ambas porciones de código estaban contenidas en el mismo archivo pero el proyecto he crecido, es hora de tomarlo en serio y el siguiente paso es refactorizar. Dependiendo de la lógica de tu proyecto puede que hayan sudedido una de los siguientes 4 casos:

## Caso a analizar

### Archivos hermanados
``` 
.
└── src/
    ├── client.py
    └── app.py
```
Es muy usual que los proyectos de cero en python en algún punto tenga este aspecto, por ejemplo, donde el cliente sea el programa principal y la aplicación sean los util, funciones recurrentes o una abstracción de clase; otro caso común es que el cliente sean scripts o tests y que aplicación sea el programa principal.

### Punto de entrada unico
``` 
.
└── src/
    ├── client.py
    └── apps/
        ├── app1.py
        └── app2.py
```
Esta estructura es muy usual cuando se tiene un punto de entrada unico para una aplicación como en un run.py o main.py; el archivo manage.py de django trabaja con este concepto.

### Carpeta clientes

``` 
.
└── src/
    ├── clients/
    │   └── client1.py
    │   └── client2.py
    └── app.py
```
Sin temor a equivocarme diré que esta es la menos común las formas de estructurar archivos en un proyecto python. El próximo caso es una version más general de la anterior y las estrategias de solución aplican practicamente igual.

``` 
.
└── src/
    ├── clients/
    │   ├── client1.py
    │   └── client2.py
    └── apps/
        ├── app1.py
        └── app2.py
```
Esta estructura es la más común cuando se trabajan en proyectos grandes. El par aplicación y cliente pueden corresponder a un paquete con sus scripts o/y tests; incluso podría ser que la aplicación sean los scripts y el cliente los tests; tal vez lo hayas visto en proyectos que incluyan notebooks y seguramente te has topado con la estructura cuando aplicación y cliente corresponden a subpaquetes de un paquete padre. Este será el principal caso a tener en cuenta en las estrategias de solución.


#local_package/module.py
#clients/script.py
#bashline

Se hace una intuitiva (y erronea) refactorizacion en clients para importar el paquete de forma relativa pero ahora al intentar ejecutarlos se presenta un error:

ImportError: attempted relative import with no known parent package

¿Porqué esto no funciona?
Dicho mal y pronto, los imports relativos solo detectan modulos contenidos dentro de un paquete y clients podra ser parte del proyecto (incluso podria ser su propio paquete) pero es "independiente" del proyecto principal.

¿Cómo hacer funcionar los clients nuevamente?

Se repasaran (por lo menos) 5 formas de lograr este objetivo, cada una con sus distintos pros y contras enlistadas de menor a mayor nivel de complejidad.

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