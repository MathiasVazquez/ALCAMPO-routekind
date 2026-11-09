# Route Kind (mapmaninterface)

An interface for tracking app

## Install the dependencies

```bash
yarn
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)

```bash
quasar dev
```

### Build the app for production

```bash
quasar build
```

### Customize the configuration

See [Configuring quasar.conf.js](https://quasar.dev/quasar-cli/quasar-conf-js).

### Leaflet corrections

En el archivo "node_modules/leaflet/dist/leaflet-src.esm.js" agregar el código "if (this.dragging) return" en la línea 7660~7665, justo antes de "if (this.dragging) {"
