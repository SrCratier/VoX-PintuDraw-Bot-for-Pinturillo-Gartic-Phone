# 🎨 VoX-PintuDraw Hi-Fi Bot

Bot de dibujo automatizado de **Alta Fidelidad (Hi-Fi)** diseñado para juegos como **Pinturillo**, **Gartic Phone** y **Skribbl.io**.

VoX-PintuDraw prioriza la **precisión, estabilidad y calidad del trazo**, utilizando la API nativa Win32 de Windows para emular movimientos reales de mouse y OpenCV para convertir imágenes en trazos optimizados.

Este enfoque evita los problemas comunes de otros bots como:

- Líneas rectas artificiales
- Saltos bruscos
- Pérdida de trazos
- Detección por patrones no humanos

---

# ✨ Características Principales

## ▫️ Motor de Precisión Hi-Fi
- Movimiento interpolado punto por punto
- Simulación de movimiento humano realista
- Previene pérdidas de trazos por limitaciones del navegador

## ▫️ Procesamiento de Imagen con OpenCV
- Conversión automática desde el portapapeles
- Detección de bordes mediante algoritmo Canny
- Optimización de contornos para dibujo eficiente

## ▫️ Sistema de Calibración Inteligente
- Calibración manual de área de dibujo
- Guarda configuración automáticamente
- Precisión adaptable a cualquier resolución

## ▫️ Control Global por Teclado
- Inicio inmediato
- Parada de emergencia
- Calibración rápida

---

# 📋 Requisitos del Sistema

**Sistema operativo:**
Windows 10 o Windows 11 (Requerido por Win32 API)

**Python:**
Python 3.8 o superior

**Dependencias:**
opencv-python
numpy
keyboard
Pillow

---

# 📦 Instalación

## 1. Clonar el repositorio

git clone https://github.com/TU_USUARIO/VoX-PintuDraw.git

## 2. Entrar en la carpeta

cd VoX-PintuDraw

## 3. Instalar dependencias

pip install -r requirements.txt

---

# ▫️ Uso

## Ejecutar el bot

python axidraw_bot.py

---

# 🎯 Calibración (Paso obligatorio)

Presiona la tecla:

F4

Luego:

1. Mueve el mouse a la esquina superior izquierda del lienzo
2. Presiona la tecla F
3. Mueve el mouse a la esquina inferior derecha
4. Presiona la tecla F

La calibración se guardará automáticamente.

---

# 🖼️ Dibujar una imagen

1. Copia cualquier imagen al portapapeles

Opciones:

- Click derecho → Copiar imagen
- Herramienta Recortes de Windows
- Ctrl + C en una imagen

2. Presiona la tecla:

HOME

El bot comenzará a dibujar automáticamente.

---

# 🛑 Detener el dibujo

Presiona la tecla:

END

La detención es inmediata y segura.

---

# ⚙️ Archivo de Configuración

El bot genera automáticamente:

config_hifi.json

Este archivo contiene:

- Coordenadas de calibración
- Ajustes de precisión

No es necesario editarlo manualmente, pero puedes eliminarlo para recalibrar.

---

# ▫️ Configuración Avanzada (Opcional)

Dentro del archivo principal, puedes ajustar:

INTERPOLATION_STEP

Controla la densidad de puntos.

Valores menores = mayor precisión  
Valores mayores = mayor velocidad  

INPUT_DELAY

Controla la velocidad del movimiento.

Valores menores = más rápido  
Valores mayores = más estable  

Configuración actual optimizada para equilibrio entre precisión y velocidad.

---

# ▫️ Arquitectura Técnica

Componentes principales:

- Win32 API → Movimiento real de mouse
- OpenCV → Procesamiento de imagen
- NumPy → Manipulación de matrices
- Pillow → Captura desde portapapeles
- Keyboard → Control global

# ⚠️ Importante

Este software está diseñado para:

- Aprendizaje
- Automatización
- Investigación técnica

Uso recomendado en:

- Partidas privadas
- Entornos de prueba
- Proyectos personales

No se recomienda su uso para afectar negativamente la experiencia de otros usuarios.

---

# 👤 Autor

VoX (SrCratier)

Proyecto VoX-PintuDraw  
Motor de dibujo Hi-Fi basado en precisión Win32

---

# ▫️ Estado del Proyecto

Versión actual: Estable

Características en desarrollo futuro:

- Optimización de rutas
- Soporte multi-color
- Interfaz gráfica
- Perfilado automático de lienzo

---

# 📜 Licencia

Uso libre para fines educativos y personales.


