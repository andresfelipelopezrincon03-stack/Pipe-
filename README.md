# Tarjeta de Juez de Boxeo 🐺

Aplicación web profesional para jueces de boxeo aficionado: cada juez califica los asaltos desde su celular y la **mesa de control** recibe todas las tarjetas en vivo. Funciona en **iOS, Android y PC** desde el navegador, sin instalar nada — y también se puede **instalar como app** (PWA) con el logo del lobo.

## Aplicación en línea

La versión en línea con mesa de control compartida en tiempo real está publicada como artefacto de Claude:

**https://claude.ai/code/artifact/b124764d-b536-4eaf-9a98-72b5404f98e7**

Comparte ese enlace con los jueces: todos los que lo abran envían sus tarjetas a la misma mesa de control.

## Funciones

- **Tarjeta de juez**: puntuación por asalto (7–10 por esquina, estilo AIBA), 3, 4 o 5 asaltos configurables.
- **Formas de resultado**: Puntos (PTS), KO, RSC, RSCI, Abandono, Descalificación (DQ) y Walkover (WO), con esquina ganadora y asalto de cierre.
- **Mesa de control en vivo**: agrupa las tarjetas por combate, calcula el resultado consolidado de los jueces y permite borrar tarjetas.
- **Copiar y compartir**: el resultado de la tarjeta o el resumen de toda la velada se copia al portapapeles o se comparte directo por WhatsApp.
- **Guardado automático**: la tarjeta se conserva en el dispositivo aunque se cierre el navegador.
- **Modo claro y oscuro** según la configuración del dispositivo.
- **Instalable (PWA)**: manifiesto, iconos del lobo y service worker con soporte sin conexión (la tarjeta funciona offline; la mesa de control necesita internet).

## Estructura

| Archivo | Descripción |
| --- | --- |
| `index.html` | Toda la aplicación (HTML, CSS y JS en un solo archivo) |
| `manifest.webmanifest` | Manifiesto PWA (nombre, colores, iconos) |
| `sw.js` | Service worker para uso sin conexión |
| `assets/lobo.png` | Mascota oficial: lobo boxeador de cuerpo completo (fondo transparente) |
| `assets/lobo-cabeza.png` | Recorte de la cabeza del lobo, usado en la cabecera y el favicon |
| `icons/` | Iconos PNG de la app (512, 192 y apple-touch 180) generados de la mascota |

## Publicar en un hosting propio

El proyecto es 100 % estático: basta con servir la carpeta en cualquier hosting con HTTPS (GitHub Pages, Netlify, Vercel…). En un hosting propio la tarjeta funciona completa en cada dispositivo; la **mesa de control compartida** entre dispositivos usa la base de datos de artefactos de Claude, por lo que solo está disponible en el enlace del artefacto de arriba.

## Instalar como app

- **Android (Chrome)**: abrir el enlace → menú ⋮ → «Agregar a la pantalla principal».
- **iOS (Safari)**: abrir el enlace → botón Compartir → «Agregar a inicio».
- **PC (Chrome/Edge)**: icono de instalación en la barra de direcciones.
