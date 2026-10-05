"""Sitio de demostración de status-sv.

Lo mínimo para desplegarlo con gunicorn, como servicio de systemd o en un
contenedor: responde /health, /version y la raíz.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent

# Una versión rota a propósito no arranca: así se prueba que el deploy vuelve
# atrás solo. Tiene que ser una excepción común: con SystemExit, gunicorn
# relanza los workers sin parar; con cualquier otra, termina con "Worker failed
# to boot" y el servicio se cae.
if (HERE / "ROTO").exists():
    raise RuntimeError("esta versión está rota a propósito: no arranca")

VERSION = (HERE / "VERSION").read_text(encoding="utf-8").strip()


def app(environ, start_response):
    routes = {
        "/health": "ok\n",
        "/version": VERSION + "\n",
        "/": f"status-sv-demo {VERSION}\n",
    }
    body = routes.get(environ.get("PATH_INFO", "/"))
    status = "200 OK" if body is not None else "404 Not Found"
    data = (body if body is not None else "no existe\n").encode("utf-8")
    start_response(status, [
        ("Content-Type", "text/plain; charset=utf-8"),
        ("Content-Length", str(len(data))),
    ])
    return [data]
