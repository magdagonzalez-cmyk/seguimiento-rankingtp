# TP Ranking - Python Flask

Proyecto convertido desde Astro a Python Flask.

## Estructura

```text
seguimiento_ranking/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── office.py
│   └── routes.py
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── favicon.svg
├── templates/
│   ├── includes/
│   ├── pages/
│   ├── base.html
│   └── index.html
├── app.py
├── requirements.txt
└── tp_ranking.db
```

## Instalar

En la terminal de VS Code:

```bash
python -m pip install -r requirements.txt
```

## Ejecutar

```bash
python app.py
```

Luego abre:

```text
http://127.0.0.1:5000
```

## Usuario de prueba

```text
RUT: 12.345.678-9
Contraseña: 123456
```

Los demás estudiantes de demostración usan la contraseña:

```text
123456
```

## Importante

No se utiliza JavaScript para el calendario. El cambio entre los 12 meses se realiza con
radio buttons de HTML y CSS.

Las rutas están centralizadas en `app/routes.py`. No se deben volver a declarar en `app.py`.

La información privada solamente se carga en `/mi-informacion` para el estudiante que inició sesión.
La página `/ranking` muestra únicamente nombre y posición.


