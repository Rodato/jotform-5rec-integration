# JotForm 5REC Integration System

Sistema automatizado para pre-llenar formularios JotForm del proyecto 5REC (Reporte Empresarial Consolidado) y enviar emails personalizados a organizaciones.

## 🚀 Características Principales

- ✅ **Pre-llenado automático** de 190+ campos del formulario
- ✅ **Mapeo validado 1:1** sin duplicados ni conflictos  
- ✅ **Envío automático de emails** con URLs personalizadas
- ✅ **Reportes detallados** de procesamiento
- ✅ **Manejo robusto de errores** y validaciones
- ✅ **100% éxito** confirmado en pruebas

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
FORM_ID=252103748882057
GMAIL_USER=tu_email@gmail.com
GMAIL_PASSWORD=tu_app_password_aqui
```

## 🗂️ Estructura del Proyecto

```
codigo/
├── config.py                 # Configuración centralizada
├── setup_validator.py        # Validador de configuración
├── form_analyzer.py          # Analizador de formulario
├── prefill_engine_v2.py      # ⭐ Motor principal de prefill
└── todas_preguntas_*.json    # Estructura del formulario JotForm
```

## 🚀 Uso Rápido

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 3. Validar Configuración
```bash
cd codigo
python3 setup_validator.py
```

### 4. Ejecutar Sistema Completo
```bash
python3 prefill_engine_v2.py
```

## 📊 Flujo de Trabajo

1. **Carga datos** desde archivo Excel con información de organizaciones
2. **Valida mapeo** de campos Excel ↔ JotForm (215 campos mapeados)
3. **Crea submissions prefilled** usando JotForm API
4. **Genera URLs únicas** de edición para cada organización
5. **Envía emails HTML** profesionales con las URLs
6. **Genera reportes** detallados de resultados

## 📧 Formato de Email

Los emails incluyen:
- 🏢 Información personalizada de la organización
- 📊 Número de campos pre-llenados
- 🔗 URL única para completar el formulario
- 📝 Instrucciones claras de uso
- 🎨 Diseño HTML profesional

## 📈 Resultados Típicos

- **Cobertura:** ~190 campos pre-llenados por organización
- **Tasa de éxito:** 100% en pruebas
- **Tiempo:** ~2-3 segundos por organización
- **Formatos:** Reportes en JSON y Excel

## 📋 Datos de Entrada

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

## 🔧 Troubleshooting

### Error: API Key inválido
```bash
# Verificar en .env
JOTFORM_API_KEY=tu_api_key_correcto
```

### Error: No se encuentran datos
- Verificar estructura del archivo Excel
- Debe tener hoja "📊 DATOS PREFILL"
- Con columnas requeridas correctamente nombradas

### Error: Email no se envía
```bash
# Verificar configuración Gmail en .env
GMAIL_USER=tu_email@gmail.com
GMAIL_PASSWORD=tu_app_password  # App password, NO contraseña normal
```

## 🛠️ Desarrollo

### Scripts Disponibles

- **`setup_validator.py`** - Validación completa de configuración y conectividad
- **`form_analyzer.py`** - Análisis detallado de estructura del formulario
- **`prefill_engine_v2.py`** - Motor principal con workflow completo

### Arquitectura

El sistema utiliza:
- **JotForm Submissions API** para crear formularios pre-llenados
- **Mapeo 1:1 validado** para eliminar duplicados y conflictos
- **URLs de edición únicas** en lugar de parámetros GET
- **Validaciones robustas** en cada paso del proceso

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