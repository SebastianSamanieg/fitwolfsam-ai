# Configuración Inicial del Proyecto

Bienvenido 👋  
Sigue estos pasos para configurar el entorno de desarrollo correctamente desde cero.

---

# 1. Requisito: Versión de Python

Este proyecto requiere:

> **Python 3.13.12 (Feb. 3, 2026)**

Verifica tu versión instalada

```bash
py -3.13 --version
```

Si no tienes la versión correcta, descárgala aquí (Windows 64-bit):

https://www.python.org/ftp/python/3.13.12/python-3.13.12-amd64.exe

---

# 2. Crear el Entorno Virtual (venv)

Para aislar las dependencias del proyecto y evitar conflictos con otras instalaciones de Python, debemos crear un entorno virtual.

Ejecuta el siguiente comando en la terminal desde la raíz del proyecto:
```bash
py -3.13 -m venv venv
```

Este comando generará una carpeta llamada `venv`, que contendrá el entorno aislado junto con las librerías y configuraciones necesarias para el proyecto.

---

# 3. Activar el Entorno Virtual

Activa el entorno según tu sistema operativo:

**Windows (PowerShell o CMD):**
```bash
.\venv\Scripts\activate
```
> **Tip:** Una vez activo, verás `(venv)` al inicio de tu terminal.


---

# 4. Instalar Dependencias

Con el entorno virtual activado:

## Actualiza pip

```bash
python -m pip install --upgrade pip
```

## Cada que instales una nueva libreria ejecuta:

```bash
pip freeze > requirements.txt
```


## Instala los requerimientos del proyecto

```bash
pip install -r requirements.txt
```

---

# 5. Configuración de Variables de Entorno

Crea tu archivo `.env` a partir de la plantilla proporcionada `.envexample`:

**Windows (PowerShell o CMD):**
```bash
copy .envexample .env
```

### Editar el archivo `.env`

Configura:

- `LOG_LEVEL` → TRACE | DEBUG | INFO | WARNING | ERROR
- `LLM_PROVIDER` → OPENAI | GOOGLE 
- Las keys requeridas

---