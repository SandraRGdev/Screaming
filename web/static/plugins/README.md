# Plugins de ScreamingWeb

Coloca tus archivos de plugin personalizados aquí. Cada archivo `.js` creará automáticamente una nueva pestaña en ScreamingWeb.

## Quick Start

1. Crea un nuevo archivo `.js` en esta carpeta (ej: `mi-plugin.js`)
2. Registra tu plugin usando la API de Plugins de ScreamingWeb
3. Refresca la app - tu nueva pestaña aparecerá automáticamente!

## Estructura de ejemplo

```javascript
ScreamingWebPlugin.register({
  // Requerido: ID único
  id: 'mi-plugin',

  // Requerido: Nombre para mostrar
  name: 'Mi Plugin',

  // Requerido: Configuración de pestaña
  tab: {
    label: 'Mi Pestaña',
    icon: '🔥',
  },

  // Se ejecuta al activar la pestaña
  onTabActivate(container, data) {
    container.innerHTML = `
      <div class="plugin-content" style="padding: 20px; overflow-y: auto; max-height: calc(100vh - 280px);">
        <h2>Mi análisis personalizado</h2>
        <p>Se encontraron ${data.urls.length} URLs!</p>
      </div>
    `;
  },

  // Opcional: Se ejecuta durante rastreos en vivo
  onDataUpdate(data) {
    if (this.isActive) {
      // Actualizar la interfaz
    }
  }
});
```

## Datos disponibles

Tu plugin recibe los mismos datos que las pestañas integradas:

- **`urls`** - Array de todas las URLs rastreadas con metadatos completos
- **`links`** - Todos los enlaces descubiertos (internos/externos)
- **`issues`** - Incidencias SEO detectadas
- **`stats`** - Estadísticas del rastreo (descubiertas, rastreadas, profundidad, velocidad)

## API Reference

### Configuración del Plugin

```javascript
{
  id: string,
  name: string,
  version: string,
  author: string,
  description: string,

  tab: {
    label: string,
    icon: string,
    position: number
  }
}
```

### Lifecycle Hooks

- `onLoad()` - Se ejecuta al cargar el plugin
- `onTabActivate(container, data)` - Se ejecuta al activar la pestaña
- `onTabDeactivate()` - Se ejecuta al cambiar de pestaña
- `onDataUpdate(data)` - Se ejecuta durante rastreos en vivo
- `onCrawlComplete(data)` - Se ejecuta al completar el rastreo

### Utilidades

Accede a las utilidades integradas vía `this.utils`:

```javascript
this.utils.showNotification(message, type) // 'success', 'error', 'info'
this.utils.formatUrl(url)
this.utils.escapeHtml(text)
```

## Estilos

Usa estas clases CSS para coincidir con el diseño de ScreamingWeb:

- `.plugin-content` - Contenedor principal
- `.plugin-header` - Sección de encabezado
- `.data-table` - Tablas (estilo automático)
- `.stat-card` - Tarjetas de estadísticas
- `.score-good` / `.score-needs-improvement` / `.score-poor` - Indicadores de puntuación

**Importante:** Siempre añade estos estilos al contenedor principal del plugin para el desplazamiento correcto:

```javascript
container.innerHTML = `
  <div class="plugin-content" style="padding: 20px; overflow-y: auto; max-height: calc(100vh - 280px);">
    <!-- Tu contenido aquí -->
  </div>
`;
```

## Plugins de ejemplo

- `_example-plugin.js` - Plantilla básica (ignorado por el cargador)
- `e-e-a-t.js` - Analizador E-E-A-T
