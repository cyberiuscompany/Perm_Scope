# 🤝 Contribuir a PermScope

¡Gracias por querer contribuir a **PermScope**! Esta herramienta permite crear módulos de análisis y recolección local para sistemas **Windows** o **Linux**.

---

## 📆 Estructura del proyecto

Cada módulo es un archivo `.py` dentro de una de estas carpetas:

- `modulos/comunes/` → Para módulos que funcionan tanto en Linux como en Windows
- `modulos/windows/` → Para módulos específicos de Windows
- `modulos/linux/` → Para módulos específicos de Linux

---

## ⚙️ Crear un nuevo módulo

1. Crea un archivo Python con el nombre adecuado (`nombre_modulo.py`) dentro de la carpeta correspondiente.
2. El archivo debe contener una función llamada `ejecutar()` que devuelva un texto (`str`) con el resultado.

### 🔧 Ejemplo básico

```python
# modulos/windows/firewall_rules.py

def ejecutar():
    import subprocess
    resultado = subprocess.getoutput("netsh advfirewall firewall show rule name=all")
    return "[+] Reglas del firewall:\n" + resultado
```

---

## ✅ Requisitos

- Debes usar `return` (no `print`) para que la salida se capture correctamente.
- Evita dependencias externas si es posible.
- Usa nombres de archivo descriptivos y en inglés si es técnico.
- Si quieres, añade tu crédito personal:

```python
# Autor: @tu_usuario (GitHub)
```

---

## 📚 Probar el módulo

Después de guardar el archivo, puedes probarlo con:

```bash
python perm_scope.py --modo consola --modulo nombre_modulo
```

---

## 📨 Enviar un Pull Request

1. Haz un fork del repositorio.
2. Crea una nueva rama para tus cambios.
3. Sube tu módulo.
4. Abre un Pull Request explicando qué hace tu módulo y en qué sistemas debería ejecutarse.

---

## 🚀 Gracias por colaborar

Tu contribución ayuda a que PermScope crezca como herramienta comunitaria.

> “Compartir conocimiento es proteger sistemas.”

