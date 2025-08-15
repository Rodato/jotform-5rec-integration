# JotForm 5REC Integration System

Sistema automatizado para pre-llenar formularios JotForm del proyecto 5REC (Reporte Empresarial Consolidado) y enviar emails personalizados a organizaciones. **Compatible con cualquier formulario JotForm.**

## 🚀 Características Principales

- ✅ **Pre-llenado automático** de 190+ campos del formulario
- ✅ **Mapeo validado 1:1** sin duplicados ni conflictos  
- ✅ **Envío automático de emails** con URLs personalizadas
- ✅ **Imágenes corporativas embebidas** en emails (CID)
- ✅ **Selección inteligente de archivos Excel** 
- ✅ **Reportes detallados** de procesamiento
- ✅ **Manejo robusto de errores** y validaciones
- ✅ **100% éxito** confirmado en pruebas
- ✅ **Sistema universal** - funciona con cualquier formulario JotForm

## 📋 Requisitos

### Dependencias Python
```bash
pip install -r requirements.txt
```

### Variables de Entorno
1. Copiar `.env.example` a `.env`
2. Configurar con tus credenciales reales:

```env
JOTFORM_API_KEY=tu_api_key_aqui
FORM_ID=tu_form_id_aqui
GMAIL_USER=tu_email@gmail.com
GMAIL_PASSWORD=tu_app_password_aqui
```

## 🗂️ Estructura del Proyecto

```
jotform-5rec-integration/
├── src/
│   ├── config.py                 # Configuración centralizada
│   ├── setup_validator.py        # Validador de configuración
│   ├── form_analyzer.py          # Analizador de formulario
│   ├── prefill_engine_v2.py      # ⭐ Motor principal de prefill
│   └── configure_email.py        # Configurador de email interactivo
├── inputs/                       # 📁 Archivos Excel con datos de organizaciones
│   └── README.md                 # Documentación de formato de datos
├── outputs/                      # 📊 Reportes y archivos de mapeo generados
│   └── README.md                 # Documentación de archivos de salida
├── img/                          # 🖼️ Imágenes corporativas para emails
│   └── README.md                 # Documentación de imágenes requeridas
├── CLAUDE.md                     # Documentación para Claude Code
├── .env.example                  # Plantilla de variables de entorno
└── requirements.txt              # Dependencias Python
```

## 🚀 Uso Rápido

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales, o usar:
cd src
python3 configure_email.py  # Configurador interactivo
```

### 3. Preparar Datos e Imágenes
```bash
# Colocar archivos Excel en inputs/
# Colocar imágenes corporativas en img/ (opcional)
```

### 4. Validar Configuración
```bash
cd src
python3 setup_validator.py
```

### 5. Ejecutar Sistema Completo
```bash
python3 prefill_engine_v2.py
# El sistema detectará automáticamente archivos Excel disponibles
```

## 📊 Flujo de Trabajo

1. **Detección automática** de archivos Excel en carpeta `inputs/`
2. **Selección inteligente** de archivo (manual o automática)
3. **Carga mapeo** desde archivos existentes o generación automática
4. **Valida mapeo** de campos Excel ↔ JotForm (215+ campos)
5. **Crea submissions prefilled** usando JotForm API
6. **Genera URLs únicas** de edición para cada organización
7. **Envía emails HTML** con imágenes corporativas embebidas
8. **Genera reportes** detallados en outputs/

## 📧 Formato de Email Mejorado

Los emails incluyen:
- 🖼️ **Imágenes corporativas embebidas** (header y botón)
- 🏢 Información personalizada de la organización
- 📊 Número de campos pre-llenados
- 🔗 URL única para completar el formulario
- 📝 Instrucciones claras de uso
- 🎨 Diseño HTML profesional responsive
- ⚡ Compatibilidad CID para máxima compatibilidad con clientes de email

## 📈 Resultados Típicos

- **Cobertura:** ~190 campos pre-llenados por organización
- **Tasa de éxito:** 100% en pruebas
- **Tiempo:** ~2-3 segundos por organización
- **Formatos:** Reportes en JSON y Excel

## 📋 Datos de Entrada

### 📁 Directorio inputs/
El sistema detecta automáticamente archivos `.xlsx` en la carpeta `inputs/`:
- **Un archivo:** Selección automática
- **Múltiples archivos:** Menú de selección interactivo
- **Modo no-interactivo:** Selecciona el primero automáticamente

### Formato Excel Requerido
El archivo Excel debe contener:
- **Hoja:** "📊 DATOS PREFILL"
- **Columnas obligatorias:**
  - `Email Destinatario` - Email donde enviar el formulario
  - `Nombre Empresa/Organización` - Nombre de la organización
  - Campos adicionales según el formulario JotForm

### Ejemplo de Estructura de Datos
```
| Email Destinatario    | Nombre Empresa/Organización | Nombre de la organización que reporta |
|-----------------------|------------------------------|---------------------------------------|
| empresa@email.com     | EMPRESA EJEMPLO S.A.S        | EMPRESA EJEMPLO S.A.S                 |
| fundacion@email.com   | FUNDACIÓN EJEMPLO            | FUNDACIÓN EJEMPLO                     |
```

## 🖼️ Imágenes Corporativas

### Directorio img/
Para emails con branding corporativo, colocar en `img/`:
- **Header:** `nombre_header.png` - Imagen superior del email (600px ancho recomendado)
- **Botón:** `nombre_boton.png` - Botón visual para acceder al formulario (200-300px ancho)

### Para 5REC específicamente:
- `5REC Franja.png` - Header corporativo
- `Imagen 5REC formulario.png` - Botón del formulario

**Nota:** El sistema funciona sin imágenes, pero se ven mejor con ellas.

## 🔧 Troubleshooting

### Error: API Key inválido
```bash
# Verificar en .env
JOTFORM_API_KEY=tu_api_key_correcto
```

### Error: No se encuentran datos
- Verificar que el archivo Excel esté en `inputs/`
- Verificar estructura del archivo Excel
- Debe tener hoja "📊 DATOS PREFILL"
- Con columnas requeridas correctamente nombradas

### Error: No se encuentran archivos Excel
```bash
# Verificar carpeta inputs
ls inputs/*.xlsx
# Colocar archivos Excel en inputs/
```

### Error: Imágenes no aparecen en email
- Verificar que las imágenes estén en `img/`
- Verificar nombres correctos de archivos
- El sistema funciona sin imágenes (modo texto)

### Error: Email no se envía
```bash
# Verificar configuración Gmail en .env
GMAIL_USER=tu_email@gmail.com
GMAIL_PASSWORD=tu_app_password  # App password, NO contraseña normal
```

## 🛠️ Desarrollo

### Scripts Disponibles

- **`configure_email.py`** - Configurador interactivo de credenciales de email
- **`setup_validator.py`** - Validación completa de configuración y conectividad
- **`form_analyzer.py`** - Análisis detallado de estructura del formulario y generación de mapeos
- **`prefill_engine_v2.py`** - Motor principal con workflow completo y nuevas funcionalidades

### Arquitectura

El sistema utiliza:
- **JotForm Submissions API** para crear formularios pre-llenados
- **Detección automática de archivos** en carpetas estructuradas
- **Mapeo inteligente** (SIMPLE_MAPPING o generación desde FORM_COMPLETE)
- **Imágenes embebidas CID** para compatibilidad universal de email
- **URLs de edición únicas** en lugar de parámetros GET
- **Validaciones robustas** en cada paso del proceso
- **Sistema universal** - adaptable a cualquier formulario JotForm

## 🤝 Contribuir

1. Fork del repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Contacto

- **Proyecto:** 5REC (Reporte Empresarial Consolidado)
- **Desarrollado para:** Integración JotForm
- **Versión:** 2.0