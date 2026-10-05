# status-sv-demo

Un sitio mínimo para probar el deploy de [status-sv](https://github.com/JuanBaez77/status-sv) en un
servidor de verdad: un deploy bueno, uno roto a propósito que vuelve atrás solo, y el primer deploy
de un proyecto nuevo.

Es una app WSGI de un archivo (`app.py`) que se corre con gunicorn y responde:

| Ruta | Respuesta |
| --- | --- |
| `/health` | `ok` |
| `/version` | el contenido de `VERSION` |
| `/` | el nombre y la versión |

## Cómo se despliega

Con el mismo repo se declaran dos proyectos en el servidor:

- **systemd** (`deploy/status-sv-demo.yaml`): gunicorn como servicio de systemd, con la unidad
  `deploy/status-sv-demo.service`. El paso `build` crea el entorno virtual e instala las
  dependencias, con el usuario `statusdemo`.
- **Docker Compose** (`deploy/status-sv-demo-docker.yaml`): la imagen del `Dockerfile`, levantada con
  `compose.yml`.

## La versión rota

Un commit que agrega el archivo `ROTO` no arranca: `app.py` termina al importarse, gunicorn no
levanta ningún worker y el proceso sale. El deploy de esa versión no queda sano, y status-sv vuelve
solo al commit anterior. Para arreglarlo, otro commit que borre `ROTO`.
