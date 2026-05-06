# Setup con OrbStack

OrbStack maneja el networking de forma diferente a Docker Desktop. Este es el setup recomendado.

## 🚀 Inicio Rápido

```bash
# 1. Iniciar Home Assistant
./dev docker-start

# 2. Abrir en el navegador
open http://localhost:8123

# 3. Ver logs
./dev docker-logs
```

## 📝 Comandos Útiles

### Gestión del Contenedor

```bash
# Iniciar (crea el contenedor si no existe)
docker run -d \
  --name my_verisure_dev \
  -p 8123:8123 \
  -v "$(pwd)/custom_components/my_verisure:/config/custom_components/my_verisure" \
  -v "$(pwd)/.devcontainer/configuration.yaml:/config/configuration.yaml" \
  -v "$(pwd)/.devcontainer/automations.yaml:/config/automations.yaml" \
  -v "$(pwd)/.devcontainer/scripts.yaml:/config/scripts.yaml" \
  -v "$(pwd)/.devcontainer/scenes.yaml:/config/scenes.yaml" \
  ghcr.io/home-assistant/home-assistant:stable

# Detener
docker stop my_verisure_dev

# Iniciar después de detener
docker start my_verisure_dev

# Reiniciar
docker restart my_verisure_dev

# Ver logs en tiempo real
docker logs -f my_verisure_dev

# Eliminar contenedor (para empezar de cero)
docker stop my_verisure_dev && docker rm my_verisure_dev
```

### Acceder al Contenedor

```bash
# Abrir shell
docker exec -it my_verisure_dev /bin/bash

# Ver logs de Home Assistant
docker exec my_verisure_dev cat /config/home-assistant.log | tail -50

# Ver logs de tu integración
docker exec my_verisure_dev cat /config/home-assistant.log | grep my_verisure

# Reiniciar Home Assistant (dentro del contenedor)
docker exec my_verisure_dev pkill -f homeassistant
```

## 🔧 Workflow de Desarrollo

### 1. Hacer cambios en el código

```bash
# Edita archivos en:
custom_components/my_verisure/

# Los cambios se reflejan automáticamente en el contenedor
# (volumen montado)
```

### 2. Reiniciar Home Assistant

```bash
# Opción 1: Desde la UI de Home Assistant
# Developer Tools → YAML → Restart

# Opción 2: Reiniciar el contenedor completo
docker restart my_verisure_dev

# Opción 3: Reiniciar solo Home Assistant
docker exec my_verisure_dev pkill -f homeassistant
```

### 3. Ver logs

```bash
# En tiempo real
docker logs -f my_verisure_dev | grep my_verisure

# Últimas 50 líneas
docker logs my_verisure_dev --tail 50

# Dentro del contenedor
docker exec my_verisure_dev tail -f /config/home-assistant.log
```

## 🌐 Acceso

### Desde el navegador

```
http://localhost:8123
```

### URLs de OrbStack

OrbStack crea URLs automáticas pero pueden dar problemas con HTTPS.
**Usa siempre `http://localhost:8123`** en su lugar.

Si ves una URL como `https://nombre_contenedor.orb.local/`:
- No la uses (dará 400 Bad Request)
- Usa `http://localhost:8123` en su lugar

### Primera vez

1. Abre http://localhost:8123
2. Completa el onboarding:
   - Crear usuario admin
   - Configurar ubicación
   - Skip integraciones iniciales
3. Añadir tu integración:
   - Settings → Devices & Services
   - Add Integration
   - Busca "My Verisure"
   - Configura con tus credenciales

## 🐛 Debugging

### Verificar que está corriendo

```bash
# Ver estado del contenedor
docker ps -f name=my_verisure_dev

# Ver procesos dentro
docker exec my_verisure_dev ps aux | grep homeassistant

# Ver puertos
docker port my_verisure_dev
```

### Verificar volúmenes

```bash
# Verificar que tu integración está montada
docker exec my_verisure_dev ls -la /config/custom_components/my_verisure

# Ver archivos de configuración
docker exec my_verisure_dev ls -la /config/
```

### Verificar logs de errores

```bash
# Errores de tu integración
docker exec my_verisure_dev cat /config/home-assistant.log | grep -i "error.*my_verisure"

# Errores generales
docker exec my_verisure_dev cat /config/home-assistant.log | grep -i error | tail -20
```

### Puerto no accesible

```bash
# 1. Verificar que el contenedor está corriendo
docker ps -f name=my_verisure_dev

# 2. Verificar mapeo de puertos
docker port my_verisure_dev
# Debe mostrar: 8123/tcp -> 0.0.0.0:8123

# 3. Probar desde terminal
python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8123/', timeout=5).status)"
# Debe mostrar: 200

# 4. Obtener IP del contenedor
docker inspect my_verisure_dev --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# 5. Probar con la IP directamente
# Abre: http://[IP_DEL_CONTENEDOR]:8123
```

## 📊 Comparación con DevContainer

| Aspecto | DevContainer | Docker Standalone (OrbStack) |
|---------|--------------|------------------------------|
| Setup | Complejo | Simple |
| Networking | Problemas con OrbStack | Funciona perfecto |
| Debugging | Integrado en Cursor | Manual con logs |
| Performance | Un poco más lento | Más rápido |
| Recomendado | Si usas Docker Desktop | Si usas OrbStack ✅ |

## 🎯 Comandos del script `./dev`

El script helper incluye comandos para OrbStack:

```bash
./dev docker-start    # Iniciar contenedor
./dev docker-stop     # Detener contenedor
./dev docker-logs     # Ver logs
./dev docker-shell    # Abrir shell

# Desarrollo
./dev test            # Ejecutar tests (fuera del contenedor)
./dev lint            # Linter
./dev format          # Formatear código
```

## ⚠️ Notas Importantes

1. **No uses el DevContainer con OrbStack** - Tiene problemas de networking
2. **Usa siempre HTTP, no HTTPS** - Home Assistant no está configurado para HTTPS
3. **Los volúmenes son live** - Edita en tu Mac, los cambios se ven inmediatamente
4. **Reinicia tras cambios en Python** - Solo cambios en YAML se recargan automáticamente
5. **La IP del contenedor puede cambiar** - Usa `localhost:8123` siempre

## 🔄 Reinicio Limpio

Si algo va mal, resetea completamente:

```bash
# 1. Detener y eliminar contenedor
docker stop my_verisure_dev
docker rm my_verisure_dev

# 2. Limpiar volúmenes persistentes (opcional)
# rm -rf ~/.homeassistant  # Si existe

# 3. Crear contenedor nuevo
./dev docker-start

# 4. Esperar 30 segundos

# 5. Abrir navegador
open http://localhost:8123
```

## ✅ Checklist

- [ ] Contenedor `my_verisure_dev` corriendo (`docker ps`)
- [ ] Puerto 8123 mapeado (`docker port my_verisure_dev`)
- [ ] Home Assistant arrancado (ver logs)
- [ ] http://localhost:8123 abre en navegador
- [ ] Onboarding completado
- [ ] Integración "My Verisure" visible en Settings

---

**¿Problemas?** Abre un issue con los logs: `docker logs my_verisure_dev > logs.txt`
