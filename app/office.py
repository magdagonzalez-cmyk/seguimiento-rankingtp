import calendar
from datetime import date


MESES = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

DIAS_SEMANA = [
    "LUNES",
    "MARTES",
    "MIÉRCOLES",
    "JUEVES",
    "VIERNES"
]

FERIADOS = {
    "2026-01-01",
    "2026-04-03",
    "2026-04-04",
    "2026-05-01",
    "2026-05-21",
    "2026-06-21",
    "2026-06-29",
    "2026-07-16",
    "2026-08-15",
    "2026-09-18",
    "2026-09-19",
    "2026-10-12",
    "2026-10-31",
    "2026-11-01",
    "2026-12-08",
    "2026-12-25",
}

AUSENCIAS = {
    "2026-03-06",
    "2026-03-17",
    "2026-05-08",
    "2026-08-14",
    "2026-10-07",
    "2026-11-06",
}

PARCIALES = {
    "2026-03-04",
    "2026-03-11",
    "2026-04-09",
    "2026-06-04",
    "2026-08-07",
    "2026-10-06",
    "2026-11-04",
}


def estado_asistencia(fecha):
    fecha_texto = fecha.isoformat()

    if fecha_texto in AUSENCIAS:
        return "ausente"

    if fecha_texto in PARCIALES:
        return "parcial"

    return "presente"


def obtener_dias_mes(anio, numero_mes):
    ultimo_dia = calendar.monthrange(anio, numero_mes)[1]
    dias = []

    for numero in range(1, ultimo_dia + 1):
        fecha = date(anio, numero_mes, numero)

        # Python: lunes=0, domingo=6.
        if fecha.weekday() >= 5:
            continue

        if fecha.isoformat() in FERIADOS:
            continue

        dias.append(
            {
                "numero": numero,
                "fecha": fecha.isoformat(),
                "estado": estado_asistencia(fecha),
            }
        )

    return dias


def obtener_calendario(anio=2026):
    return [
        {
            "nombre": MESES[indice],
            "numero": indice + 1,
            "dias": obtener_dias_mes(anio, indice + 1),
        }
        for indice in range(12)
    ]
