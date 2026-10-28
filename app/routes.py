from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)

from .models import (
    buscar_estudiante,
    estudiantes_por_curso,
    obtener_estudiante,
    obtener_notas,
    obtener_posicion,
    obtener_promedio,
)
from .office import (
    DIAS_SEMANA,
    obtener_calendario,
)


bp = Blueprint("main", __name__)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped


@bp.context_processor
def datos_globales():
    return {
        "usuario": session.get("usuario")
    }


@bp.get("/")
def index():
    if session.get("usuario"):
        return redirect(url_for("main.rankingtp"))

    return render_template(
        "index.html",
        title="Iniciar sesión | TP Ranking",
        description="Acceso al sistema TP Ranking.",
    )


@bp.get("/login")
def login():
    if session.get("usuario"):
        return redirect(url_for("main.rankingtp"))

    return render_template(
        "pages/login.html",
        title="Iniciar sesión | TP Ranking",
        description="Inicio de sesión para estudiantes de TP Ranking.",
    )


@bp.post("/api/login")
def api_login():
    rut = request.form.get("rut", "").strip()
    password = request.form.get("password", "")

    estudiante = buscar_estudiante(rut, password)

    if estudiante is None:
        return render_template(
            "pages/login.html",
            title="Iniciar sesión | TP Ranking",
            description="Inicio de sesión para estudiantes de TP Ranking.",
            error="RUT o contraseña incorrectos.",
            rut=rut,
        ), 401

    session.clear()

    session["usuario"] = {
        "id": estudiante["id"],
        "rut": estudiante["rut"],
        "nombre": estudiante["nombre"],
        "curso": estudiante["curso"],
    }

    return redirect(url_for("main.rankingtp"), code=303)


@bp.post("/api/logout")
def api_logout():
    session.clear()
    return redirect(url_for("main.index"), code=303)


@bp.get("/rankingtp")
@login_required
def rankingtp():
    return render_template(
        "pages/rankingtp.html",
        title="TP Ranking",
        description="Sistema de ranking para estudiantes TP.",
    )


@bp.get("/ranking")
@login_required
def ranking():
    ranking_3 = estudiantes_por_curso("3° Medio TP")
    ranking_4 = estudiantes_por_curso("4° Medio TP")

    return render_template(
        "pages/ranking.html",
        title="Ranking | TP Ranking",
        description="Ranking de estudiantes de 3° y 4° Medio TP.",
        ranking_3=ranking_3,
        ranking_4=ranking_4,
    )


@bp.get("/asignaturas")
@login_required
def asignaturas():
    return render_template(
        "pages/asignaturas.html",
        title="Asignaturas | TP Ranking",
        description="Asignaturas de los estudiantes TP.",
    )


@bp.get("/nosotros")
@login_required
def nosotros():
    return render_template(
        "pages/nosotros.html",
        title="Nosotros | Ranking TP",
        description="Información sobre el proyecto Ranking TP.",
    )


@bp.get("/mi-informacion")
@login_required
def mi_informacion():
    usuario = session["usuario"]

    estudiante = obtener_estudiante(usuario["rut"])

    if estudiante is None:
        session.clear()
        return redirect(url_for("main.login"))

    notas = obtener_notas(estudiante["id"])
    promedio = obtener_promedio(estudiante["id"])
    posicion, total = obtener_posicion(
        estudiante["id"],
        estudiante["curso"],
    )

    meses = obtener_calendario(2026)

    return render_template(
        "pages/mi-informacion.html",
        title="Mi información | TP Ranking",
        description="Información académica y asistencia del estudiante.",
        estudiante=estudiante,
        notas=notas,
        promedio=promedio,
        posicion=posicion,
        total_estudiantes=total,
        cantidad_anotaciones=1 if estudiante["anotacion"] else 0,
        meses=meses,
        dias_semana=DIAS_SEMANA,
        anio=2026,
    )
