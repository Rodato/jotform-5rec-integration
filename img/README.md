# Directorio de Imágenes / Images Directory

Este directorio contiene las imágenes corporativas utilizadas en los emails del sistema.

## Archivos requeridos / Required files:

### Para 5REC:
- `5REC Franja.png` - Imagen de encabezado/header para emails
- `Imagen 5REC formulario.png` - Botón visual para acceder al formulario

### Para otros proyectos:
Puedes reemplazar estas imágenes con las de tu organización:
- **Header image**: Imagen que aparece en la parte superior del email (recomendado: 600px ancho)
- **Button image**: Imagen que actúa como botón para acceder al formulario (recomendado: 200-300px ancho)

## Uso en el código:
El sistema busca automáticamente estas imágenes y las embebe en los emails usando Content-ID (CID) para máxima compatibilidad con clientes de correo.

Si las imágenes no existen, el sistema funcionará igualmente pero sin las imágenes corporativas en los emails.