# Catálogo de archivos

`FILE_CATALOG.csv` se genera con `python tools/build_file_catalog.py`. Tiene rutas relativas, categoría, tamaño en bytes y SHA-256. Se excluyen el propio catálogo, `.git`, `__pycache__` y `.pyc`. Regenera después de añadir o cambiar archivos.
