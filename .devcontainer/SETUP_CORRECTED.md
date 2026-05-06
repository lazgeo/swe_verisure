# DevContainer Setup - Instrucciones Actualizadas

## ✅ Imagen descargada correctamente

La imagen de Home Assistant ya está descargada y lista para usar.

## 🚀 Cómo abrir el DevContainer en Cursor

### Paso 1: Reabrir en DevContainer

En Cursor, presiona `Cmd+Shift+P` y busca:
```
Remote-Containers: Reopen in Container
```

O haz click en el botón verde/azul de la esquina inferior izquierda y selecciona "Reopen in Container".

### Paso 2: Esperar la construcción

Primera vez tomará unos 2-3 minutos para:
- Montar volúmenes
- Instalar extensiones de Python
- Configurar el entorno

### Paso 3: Verificar que estás dentro

En la esquina inferior izquierda verás:
**"Dev Container: My Verisure Development"**

## 🏠 Comandos dentro del DevContainer

Una vez dentro del contenedor, abre el terminal (`` Cmd+` ``) y usa:

### Iniciar Home Assistant

```bash
# Opción 1: Usando el script
/workspaces/my_verisure/.devcontainer/start.sh

# Opción 2: Comando directo
python3 -m homeassistant --config /config --debug

# Opción 3: En background
python3 -m homeassistant --config /config &
```

### Otros comandos útiles

```bash
# Ver logs
tail -f /config/home-assistant.log

# Ver logs solo de tu integración
tail -f /config/home-assistant.log | grep my_verisure

# Verificar configuración
python3 -m homeassistant --config /config --script check_config

# Detener Home Assistant
pkill -f homeassistant

# Verificar si está corriendo
ps aux | grep homeassistant
```

### Acceder a Home Assistant

Abre tu navegador en:
```
http://localhost:7123
```

## 🔧 Tareas de Cursor/VS Code

También puedes usar las tareas configuradas:

1. Presiona `Cmd+Shift+P`
2. Escribe: `Tasks: Run Task`
3. Selecciona una tarea:
   - **Run Home Assistant** - Inicia HA
   - **Restart Home Assistant** - Reinicia HA
   - **Check Config** - Verifica configuración
   - **Run Tests** - Ejecuta tests

## 📝 Workflow de Desarrollo

```bash
# 1. Dentro del DevContainer, inicia HA
python3 -m homeassistant --config /config &

# 2. Haz cambios en tu código
# Edita: custom_components/my_verisure/...

# 3. Reinicia Home Assistant
pkill -f homeassistant
sleep 2
python3 -m homeassistant --config /config &

# 4. Verifica en el navegador
# http://localhost:7123

# 5. Ve los logs
tail -f /config/home-assistant.log | grep my_verisure
```

## 🐛 Debugging

Para debugging con breakpoints:

1. Añade breakpoints (click en el margen izquierdo)
2. Presiona `F5`
3. Selecciona **Home Assistant (DevContainer)**
4. El código se detendrá en los breakpoints

## 📂 Estructura de Directorios

Dentro del contenedor:
```
/config/                          # Config de Home Assistant
├── configuration.yaml            # Tu config personalizada
├── custom_components/
│   └── my_verisure/             # Tu integración (montada)
├── home-assistant.log           # Logs
└── ...

/workspaces/my_verisure/         # Tu código fuente
└── custom_components/
    └── my_verisure/             # Código real (editalo aquí)
```

## ⚠️ Notas Importantes

1. **No uses `container start`** - Este comando no existe en esta configuración
2. **Usa `python3 -m homeassistant`** directamente
3. **Los cambios** en el código se reflejan instantáneamente (volumen montado)
4. **Reinicia HA** después de cambios en código Python
5. **Recarga YAML** para cambios en configuración

## 🆘 Solución de Problemas

### HA no inicia

```bash
# Ver el error completo
python3 -m homeassistant --config /config --debug

# Verificar la configuración
python3 -m homeassistant --config /config --script check_config
```

### Puerto no accesible

1. Verifica en Cursor que el puerto 7123 está forwarded
2. Mira el panel "Ports" (abajo)
3. Intenta con http://127.0.0.1:7123

### Integración no aparece

```bash
# Verifica que el mount funcionó
ls -la /config/custom_components/my_verisure

# Verifica logs de errores
grep -i error /config/home-assistant.log | grep my_verisure
```

### Cambios no se reflejan

1. Asegúrate de editar en `/workspaces/my_verisure/custom_components/`
2. Reinicia Home Assistant:
   ```bash
   pkill -f homeassistant
   python3 -m homeassistant --config /config &
   ```

## ✅ Checklist de Primer Uso

- [ ] Cursor abierto en el proyecto
- [ ] "Reopen in Container" ejecutado
- [ ] Terminal abierto (`` Cmd+` ``)
- [ ] Home Assistant iniciado con `python3 -m homeassistant --config /config &`
- [ ] Navegador en http://localhost:7123
- [ ] Onboarding completado (crear usuario)
- [ ] Integración "My Verisure" añadida

## 🎯 Próximos Pasos

Una vez que Home Assistant esté corriendo:

1. Ve a http://localhost:7123
2. Completa el onboarding inicial
3. Ve a **Settings → Devices & Services**
4. Click en **Add Integration**
5. Busca "My Verisure"
6. Configura con tus credenciales

¡Listo para desarrollar! 🎉
