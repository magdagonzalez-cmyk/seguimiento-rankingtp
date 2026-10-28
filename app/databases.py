import sqlite3
from pathlib import Path

from .config import Config


def get_connection():
    connection = sqlite3.connect(Config.DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def setup_database(app=None):
    Path(Config.DATABASE).parent.mkdir(parents=True, exist_ok=True)

    connection = get_connection()

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rut TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
            curso TEXT NOT NULL,
            anotacion TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            asignatura TEXT NOT NULL,
            nota REAL NOT NULL,
            FOREIGN KEY (estudiante_id)
                REFERENCES estudiantes(id)
                ON DELETE CASCADE
        );
        """
    )

    # Cargar datos de demostración solamente si la base está vacía.
    total = connection.execute(
        "SELECT COUNT(*) FROM estudiantes"
    ).fetchone()[0]

    if total == 0:
        estudiantes = [
            ("11.111.111-1", "123456", "María González", "3° Medio TP", ""),
            ("11.111.111-2", "123456", "Pedro Soto", "3° Medio TP", ""),
            ("11.111.111-3", "123456", "Camila Rojas", "3° Medio TP", ""),
            ("12.345.678-9", "123456", "Juan Pérez", "3° Medio TP",
             "Atrasos e inasistencias registrados durante el período académico."),
            ("11.111.111-5", "123456", "Diego Muñoz", "3° Medio TP", ""),
            ("11.111.111-6", "123456", "Antonia Silva", "3° Medio TP", ""),
            ("11.111.111-7", "123456", "Matías Torres", "3° Medio TP", ""),
            ("11.111.111-8", "123456", "Valentina Díaz", "3° Medio TP", ""),

            ("22.222.222-1", "123456", "Sofía Pérez", "4° Medio TP", ""),
            ("22.222.222-2", "123456", "Nicolás Torres", "4° Medio TP", ""),
            ("22.222.222-3", "123456", "Valentina Soto", "4° Medio TP", ""),
            ("22.222.222-4", "123456", "Martín Rojas", "4° Medio TP", ""),
            ("22.222.222-5", "123456", "Fernanda Díaz", "4° Medio TP", ""),
            ("22.222.222-6", "123456", "Tomás Silva", "4° Medio TP", ""),
            ("22.222.222-7", "123456", "Javiera Muñoz", "4° Medio TP", ""),
            ("22.222.222-8", "123456", "Benjamín Castro", "4° Medio TP", ""),
        ]

        cursor = connection.executemany(
            """
            INSERT INTO estudiantes
                (rut, password, nombre, curso, anotacion)
            VALUES (?, ?, ?, ?, ?)
            """,
            estudiantes
        )

        # Notas: el promedio se calcula automáticamente.
        notas = {
            "María González": [6.6, 6.5, 6.7, 6.6],
            "Pedro Soto": [6.4, 6.3, 6.5, 6.4],
            "Camila Rojas": [6.2, 6.1, 6.3, 6.2],
            "Juan Pérez": [6.1, 5.8, 6.0, 6.1],
            "Diego Muñoz": [5.9, 5.8, 5.9, 6.0],
            "Antonia Silva": [5.8, 5.7, 5.9, 5.8],
            "Matías Torres": [5.7, 5.6, 5.8, 5.7],
            "Valentina Díaz": [5.6, 5.5, 5.7, 5.6],

            "Sofía Pérez": [6.8, 6.7, 6.9, 6.8],
            "Nicolás Torres": [6.6, 6.5, 6.7, 6.6],
            "Valentina Soto": [6.4, 6.3, 6.5, 6.4],
            "Martín Rojas": [6.2, 6.1, 6.3, 6.2],
            "Fernanda Díaz": [6.0, 5.9, 6.1, 6.0],
            "Tomás Silva": [5.9, 5.8, 6.0, 5.9],
            "Javiera Muñoz": [5.8, 5.7, 5.9, 5.8],
            "Benjamín Castro": [5.6, 5.5, 5.7, 5.6],
        }

        for nombre, valores in notas.items():
            estudiante = connection.execute(
                "SELECT id FROM estudiantes WHERE nombre = ?",
                (nombre,)
            ).fetchone()

            asignaturas = [
                "Infraestructura TI",
                "Diseño de Base de Datos",
                "Programación y Algoritmos",
                "Desarrollo Web",
            ]

            connection.executemany(
                """
                INSERT INTO notas
                    (estudiante_id, asignatura, nota)
                VALUES (?, ?, ?)
                """,
                [
                    (estudiante["id"], asignatura, nota)
                    for asignatura, nota in zip(asignaturas, valores)
                ]
            )

    connection.commit()
    connection.close()
