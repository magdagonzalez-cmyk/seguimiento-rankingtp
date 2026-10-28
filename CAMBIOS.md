# Conversión de Astro a Python Flask

Este proyecto parte de la versión Astro que se entregó y la convierte a la estructura Flask mostrada por el estudiante.

## Equivalencias

| Astro | Flask |
|---|---|
| `src/layouts/Layout.astro` | `templates/base.html` |
| `src/components/Header.astro` | `templates/includes/header.html` |
| `src/components/Footer.astro` | `templates/includes/footer.html` |
| `src/pages/index.astro` | `templates/index.html` |
| `src/pages/login.astro` | `templates/pages/login.html` |
| `src/pages/ranking.astro` | `templates/pages/ranking.html` |
| `src/pages/rankingtp.astro` | `templates/pages/rankingtp.html` |
| `src/pages/asignaturas.astro` | `templates/pages/asignaturas.html` |
| `src/pages/nosotros.astro` | `templates/pages/nosotros.html` |
| `src/pages/mi-informacion.astro` | `templates/pages/mi-informacion.html` |
| `src/pages/api/login.ts` | `POST /api/login` en `app/routes.py` |
| `src/pages/api/logout.ts` | `POST /api/logout` en `app/routes.py` |
| `src/middleware.ts` | `login_required` en `app/routes.py` |
| `src/styles/global.css` | `static/css/style.css` |

## Importante

Todas las rutas están en un único lugar:

```text
app/routes.py
```

El archivo `app.py` solamente crea la aplicación y la ejecuta. Esto evita el error:

```text
AssertionError: View function mapping is overwriting an existing endpoint function
```

No hay rutas duplicadas.

## JavaScript

El calendario conserva el funcionamiento original sin JavaScript.

Los 12 meses se cambian usando:

- radio buttons HTML
- labels
- CSS `transform`

`static/js/script.js` se mantiene solamente como archivo de la estructura, pero no es necesario para el funcionamiento.

## Base de datos

Se incluye `tp_ranking.db` con datos de demostración.

Usuario principal:

```text
RUT: 12.345.678-9
Contraseña: 123456
```

La base contiene estudiantes de:

- 3° Medio TP
- 4° Medio TP

El ranking público muestra solamente:

- posición
- nombre

La página privada muestra solamente al estudiante que inició sesión:

- posición
- promedio
- notas
- anotación
- asistencia

## Instalación

```bash
python -m pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

Abrir:

```text
http://127.0.0.1:5000
```
