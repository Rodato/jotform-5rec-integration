# JotForm 5REC Prefill Engine v2.0

Sistema automatizado de prefill para formularios JotForm del proyecto 5REC con generación de tabla Excel para envío manual de emails.

## 🚀 Características Principales

- **Motor de Prefill**: Crea submissions prefilled con mapeo mejorado sin truncamiento
- **Sistema de Monitoreo Avanzado**: Tracking completo de respuestas con clasificación Prefill vs Manual
- **Generación Excel**: Tabla profesional con empresa, email y links de prefill
- **Templates Email**: Plantillas listas para copiar/pegar en emails corporativos
- **Sin Autenticación Email**: Evita problemas con cuentas corporativas Microsoft
- **Mapeo Inteligente**: Fuzzy matching mejorado sin límites de caracteres
- **Filtrado Inteligente**: Exclusión automática de campos informativos en monitoreo
- **Reportes Completos**: Estadísticas detalladas y logs de procesamiento

## 📁 Estructura del Proyecto

```
jotform_final/
├── src/                              # Código fuente
│   ├── prefill_engine_v2.py         # Motor principal de prefill
│   ├── form_monitor_v2.py           # Sistema de monitoreo avanzado
│   ├── excel_generator.py           # Generador de tabla Excel
│   ├── run_excel_only.py            # Script solo para Excel
│   ├── form_analyzer.py             # Analizador de formularios
│   ├── config.py                    # Configuración del sistema
│   └── configure_email.py           # Configurador de credenciales
├── inputs/                           # Archivos Excel con datos de entrada
├── outputs/                          # Reportes y archivos generados
├── img/                              # Imágenes del proyecto
└── requirements.txt                  # Dependencias Python
```

## 🛠️ Instalación

1. **Clonar repositorio:**
```bash
git clone <repository-url>
cd jotform_final
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar credenciales:**
```bash
cd src
python configure_email.py
```

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# JotForm API Configuration
JOTFORM_API_KEY=tu_api_key_aqui
FORM_ID=252195670354662

# Email Configuration (opcional)
GMAIL_USER=tu_email@dominio.com
GMAIL_PASSWORD=tu_password_o_app_password
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587

# Project Settings
PROJECT_NAME=5REC
```

### Formato Archivo Excel Input

El archivo Excel debe tener una hoja llamada **"📊 DATOS PREFILL"** con columnas como:
- `Nombre Empresa/Organización`
- `Email Destinatario`
- Otros campos que mapeen a campos del formulario JotForm

## 📊 Uso Principal - Solo Excel (Recomendado)

### Opción 1: Script Dedicado
```bash
cd src
python run_excel_only.py
```

### Opción 2: Motor Principal
```bash
cd src
python prefill_engine_v2.py
# Seleccionar opción 1 (Solo Excel)
```

## 📋 Archivos Generados

El sistema genera en `outputs/`:

1. **`LINKS_PREFILL_YYYYMMDD_HHMMSS.xlsx`**
   - Tabla con empresa, email, estado prefill y link
   - Hoja de resumen con estadísticas
   - Formato profesional con colores

2. **`EMAIL_TEMPLATES_YYYYMMDD_HHMMSS.txt`**
   - Templates de email personalizados
   - Listos para copiar/pegar

3. **`PREFILL_ENGINE_V2_REPORT_YYYYMMDD_HHMMSS.json`**
   - Reporte técnico detallado
   - Estadísticas de procesamiento

4. **`ESTADO_EMPRESAS_YYYYMMDD_HHMMSS.xlsx`** (Monitoreo)
   - Estado de cada empresa (Completado/Pendiente)
   - Clasificación Prefill vs Manual
   - Scores de matching fuzzy

5. **`RESPUESTAS_DETALLADAS_YYYYMMDD_HHMMSS.xlsx`** (Monitoreo)
   - Respuestas completas por empresa
   - Solo campos que requieren respuesta
   - Filtrado inteligente de elementos informativos

## 🔄 Flujo de Trabajo

1. **Preparar datos**: Colocar archivo Excel en `inputs/`
2. **Ejecutar sistema**: `python run_excel_only.py`
3. **Abrir Excel**: Revisar tabla generada en `outputs/`
4. **Enviar emails**: Copiar links y usar email corporativo manualmente
5. **Monitorear respuestas**: `python form_monitor_v2.py` para tracking avanzado
6. **Análisis**: Revisar tablas de estado y respuestas detalladas

## 📧 Envío Manual de Emails

### Usar Tabla Excel:
1. Abrir archivo `LINKS_PREFILL_*.xlsx`
2. Copiar link de columna "Link de Prefill"
3. Componer email en cliente corporativo
4. Pegar link personalizado para cada empresa

### Usar Templates:
1. Abrir archivo `EMAIL_TEMPLATES_*.txt`
2. Copiar template correspondiente a cada empresa
3. Pegar en email corporativo
4. Ajustar personalización si es necesario

## 📊 Monitoreo de Respuestas

### Ejecutar Monitoreo:
```bash
cd src
python form_monitor_v2.py
```

### Características del Monitoreo v2:
- **Clasificación Automática**: Identifica respuestas Prefill vs Manual usando fuzzy matching
- **Filtrado Inteligente**: Excluye campos informativos (títulos, instrucciones, botones)
- **Tracking Completo**: Estado por empresa con fechas y scores de matching
- **Tablas Detalladas**: Respuestas completas organizadas por empresa y pregunta
- **Empresas Pendientes**: Identifica prefills enviados pero no respondidos

## 🔍 Troubleshooting

### Error: No se encontraron archivos de mapeo
- Ejecutar `form_analyzer.py` primero para generar mapeo

### Error: No se encontraron archivos Excel
- Verificar que hay archivos `.xlsx` en carpeta `inputs/`
- Verificar que tienen hoja "📊 DATOS PREFILL"

### Links de prefill no funcionan
- Verificar JOTFORM_API_KEY en configuración
- Verificar FORM_ID correcto
- Revisar logs en archivo de reporte JSON

## 🔐 Seguridad

- **API Keys**: Nunca commitear credenciales al repositorio
- **Datos sensibles**: Archivos Excel con datos empresariales no se commitean
- **Logs**: Los reportes pueden contener información sensible

## 📈 Características Avanzadas

### Mapeo Automático Mejorado
- Mapeo fuzzy mejorado sin truncamiento de texto (removido límite [:50])
- Validación automática de tipos de datos
- Limpieza inteligente de datos
- Mejor correlación entre campos Excel y JotForm

### Procesamiento por Lotes
- Procesamiento eficiente de múltiples organizaciones
- Manejo de errores individual por empresa
- Pausas automáticas entre requests API

### Reportes Detallados
- Estadísticas de éxito/fallo
- Tracking de campos mapeados
- Logs detallados para debugging
- Monitoreo avanzado con clasificación automática
- Filtrado inteligente de campos informativos
- Análisis de respuestas con scoring fuzzy

## 🤝 Contribución

1. Fork del repositorio
2. Crear branch para feature
3. Commit de cambios
4. Push a branch
5. Crear Pull Request

## 📄 Licencia

Este proyecto es parte del sistema 5REC y está sujeto a las políticas de la organización.

---

**Última actualización**: 2025-08-23  
**Versión**: 2.0 - Sistema con monitoreo avanzado