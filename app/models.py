from .databases import get_connection


def buscar_estudiante(rut, password):
    connection = get_connection()

    estudiante = connection.execute(
        """
        SELECT id, rut, nombre, curso, anotacion
        FROM estudiantes
        WHERE rut = ? AND password = ?
        """,
        (rut, password)
    ).fetchone()

    connection.close()

    return dict(estudiante) if estudiante else None


def obtener_estudiante(rut):
    connection = get_connection()

    estudiante = connection.execute(
        """
        SELECT id, rut, nombre, curso, anotacion
        FROM estudiantes
        WHERE rut = ?
        """,
        (rut,)
    ).fetchone()

    connection.close()

    return dict(estudiante) if estudiante else None


def obtener_notas(estudiante_id):
    connection = get_connection()

    filas = connection.execute(
        """
        SELECT asignatura, nota
        FROM notas
        WHERE estudiante_id = ?
        ORDER BY id
        """,
        (estudiante_id,)
    ).fetchall()

    connection.close()

    return [
        {
            "asignatura": fila["asignatura"],
            "nota": fila["nota"],
        }
        for fila in filas
    ]


def obtener_promedio(estudiante_id):
    connection = get_connection()

    fila = connection.execute(
        """
        SELECT AVG(nota) AS promedio
        FROM notas
        WHERE estudiante_id = ?
        """,
        (estudiante_id,)
    ).fetchone()

    connection.close()

    return round(float(fila["promedio"] or 0), 1)


def estudiantes_por_curso(curso):
    connection = get_connection()

    filas = connection.execute(
        """
        SELECT
            e.id,
            e.nombre,
            e.curso,
            ROUND(AVG(n.nota), 1) AS promedio
        FROM estudiantes e
        LEFT JOIN notas n
            ON n.estudiante_id = e.id
        WHERE e.curso = ?
        GROUP BY e.id, e.nombre, e.curso
        ORDER BY promedio DESC, e.nombre ASC
        """,
        (curso,)
    ).fetchall()

    connection.close()

    resultado = []

    for posicion, fila in enumerate(filas, start=1):
        resultado.append(
            {
                "id": fila["id"],
                "nombre": fila["nombre"],
                "curso": fila["curso"],
                "promedio": float(fila["promedio"] or 0),
                "posicion": posicion,
            }
        )

    return resultado


def obtener_posicion(estudiante_id, curso):
    ranking = estudiantes_por_curso(curso)

    for estudiante in ranking:
        if estudiante["id"] == estudiante_id:
            return estudiante["posicion"], len(ranking)

    return None, len(ranking)
