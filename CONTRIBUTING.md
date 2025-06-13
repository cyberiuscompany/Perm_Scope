# 🤝 Contribuir a PermScope

¡Gracias por querer contribuir a PermScope! Esta herramienta permite crear módulos de análisis locales para sistemas Windows o Linux.

---

## 📦 Estructura

Cada módulo es un archivo `.py` dentro de:

- `modulos/comunes/` → Funciona en ambos sistemas.
- `modulos/windows/` → Solo para Windows.
- `modulos/linux/` → Solo para Linux.

---

## 🛠 Cómo crear un módulo

1. Crea un archivo Python con el nombre `nombre_modulo.py` dentro de la carpeta correcta.
2. Debe incluir **una función `ejecutar()`** que retorne una cadena (`str`) con el resultado.

### 🧪 Ejemplo:

```python
# modulos/windows/firewall_rules.py

def ejecutar():
    import subprocess
    resultado = subprocess.getoutput("netsh advfirewall firewall show rule name=all")
    return "[+] Reglas del firewall:\n" + resultado
