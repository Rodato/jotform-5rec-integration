# Directorio de Salida / Output Directory

Este directorio contiene todos los archivos generados por el sistema durante la ejecución.

## Tipos de archivos generados:

### 📊 Archivos de análisis de formulario:
- `FORM_ANALYSIS_YYYYMMDD_HHMMSS.csv` - Análisis de campos en formato CSV
- `FORM_ANALYSIS_YYYYMMDD_HHMMSS.xlsx` - Análisis detallado en Excel con múltiples hojas
- `FORM_COMPLETE_YYYYMMDD_HHMMSS.json` - Metadatos completos del formulario

### 🗺️ Archivos de mapeo:
- `SIMPLE_MAPPING_YYYYMMDD_HHMMSS.json` - Mapeo directo de columnas Excel → IDs de campos
- `CLEAN_MAPPING_YYYYMMDD_HHMMSS.json` - Mapeo limpio y validado

### 📈 Reportes de ejecución:
- `PREFILL_ENGINE_V2_REPORT_YYYYMMDD_HHMMSS.json` - Reporte detallado en JSON
- `PREFILL_ENGINE_V2_REPORT_YYYYMMDD_HHMMSS.xlsx` - Reporte en formato Excel

## Generación de archivos:

### Para análisis de formulario:
```bash
python src/form_analyzer.py
```
Genera archivos de análisis y metadatos del formulario.

### Para reportes de mapeo:
Los archivos de mapeo se pueden generar usando herramientas adicionales o copiarse desde implementaciones previas.

### Para reportes de ejecución:
```bash
python src/prefill_engine_v2.py
```
Genera reportes automáticamente después de procesar las organizaciones.

## Uso del sistema:
- El sistema busca automáticamente archivos `SIMPLE_MAPPING_*.json` 
- Si no los encuentra, puede generar mapeo desde archivos `FORM_COMPLETE_*.json`
- Los reportes incluyen estadísticas de éxito, errores y URLs generadas
- Todos los archivos incluyen timestamp para mantener historial

## Compatibilidad:
El sistema funciona con cualquier formulario de JotForm, no solo 5REC. Los archivos de mapeo se adaptan automáticamente a la estructura del formulario configurado.