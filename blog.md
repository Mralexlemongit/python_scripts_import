# 5 métodos para invocar un proyecto desde tus scripts

Nivel conocimiento: Python intermedio (Imports, ambientes, comandos)
Tiempo de lectura: 30 minutos

Esta semana me he encontrado con un problema típico al desarrollar Python y quise aprovechar para compartir distintas estrategias para solucionarlo:

Se esta construyendo un paquete de Python ademas de tener scripts que se ejecutan desde consola. El proyecto ha crecido, es hora de tomarlo en serio y el siguiente paso es estructurar. Sobre la raíz se crean 2 carpetas, una para el paquete principal y otra para los scripts.

#local_package/module.py
#scripts/script.py
#bashline

Se hace una intuitiva (y erronea) refactorizacion en scripts para importar el paquete de forma relativa pero ahora al intentar ejecutarlos se presenta un error:

ImportError: attempted relative import with no known parent package

¿Porqué esto no funciona?
Dicho mal y pronto, los imports relativos solo detectan modulos contenidos dentro de un paquete y scripts podra ser parte del proyecto (incluso podria ser su propio paquete) pero es "independiente" del proyecto principal.

¿Cómo hacer funcionar los scripts nuevamente?

Se repasaran (por lo menos) 5 formas de lograr este objetivo, cada una con sus distintos pros y contras enlistadas de menor a mayor nivel de complejidad.

===== Subencarpetar los scripts:
Si el problema es que los scripts no son parte del paquete, ¿Porqué no incluirlos en este? La idea es convertir a scripts en un subpaquete y hacer el un import absoluto del contenido del paquete.
• recomendado para proyectos pequeños y medianos o donde no importa tener toda la logica en la mima subraiz
• No se recomienda si se quiere usar este metodo para dos paquetes sobre raiz
• El mas sencillo de todos
• Mantiene la logica mal estructurada
• Los scripts no pueden invocarse desde cualquier lugar?
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

REFERENCIAS
https://www.datasciencelearner.com/importerror-attempted-relative-import-parent-package/