# DevContainer Configuration

This directory contains the Cursor/VS Code DevContainer configuration for developing the My Verisure integration with a full Home Assistant environment.

**Note:** Cursor is built on VS Code, so all DevContainer features work identically in both editors.

## What's Included

### `devcontainer.json`

Main DevContainer configuration:

- **Base Image:** `ghcr.io/home-assistant/devcontainer:stable` (official HA dev image)
- **Port:** Home Assistant runs on port 7123 (mapped from container's 8123)
- **Mount:** Your `custom_components/my_verisure` is mounted into the container's HA config
- **Extensions:** Python, Pylance, Black formatter, YAML support
- **Settings:** Python 3 interpreter, linting, formatting on save, pytest enabled

### `configuration.yaml`

Home Assistant configuration for development:

- **Debug logging** for `my_verisure` integration
- **Developer tools** enabled
- **Recorder** using SQLite in /tmp (lightweight, auto-cleanup)
- **Frontend** in development mode
- Includes example automations, scenes, and scripts

### `automations.yaml`

Example automations for testing:

- Logs when alarm state changes
- Add your own test automations here

### `scripts.yaml`

Ready-to-use scripts for testing services:

- `test_arm_away` - Test arming in away mode
- `test_arm_home` - Test arming in home mode
- `test_disarm` - Test disarming

Edit `YOUR_INSTALLATION_ID` to match your actual installation.

### `scenes.yaml`

Placeholder for test scenes. Add your own as needed.

## How It Works

1. **Cursor/VS Code detects** `.devcontainer/devcontainer.json`
2. **Docker builds** a container with Home Assistant pre-installed
3. **Your integration** is mounted at `/workspaces/core/config/custom_components/my_verisure`
4. **Configuration files** from this directory are used for HA config
5. **Extensions and settings** are automatically applied

## First Time Setup

```bash
# 1. Open project in Cursor (or VS Code)
cursor .
# Or: code .

# 2. Cursor/VS Code will prompt: "Reopen in Container"
# Click it or: Cmd+Shift+P → "Remote-Containers: Reopen in Container"

# 3. Wait for container to build (~5 minutes first time)

# 4. Start Home Assistant
container start

# 5. Open browser
http://localhost:7123
```

## Development Workflow

### Make Changes

1. Edit files in `custom_components/my_verisure/`
2. Changes are immediately reflected in the container (mounted volume)

### Restart Home Assistant

After code changes:

```bash
# Option 1: From terminal
container restart

# Option 2: From Cursor/VS Code
# Cmd+Shift+P → Tasks: Run Task → Restart Home Assistant

# Option 3: From Home Assistant UI
# Developer Tools → YAML → Restart
```

### View Logs

```bash
# Real-time logs filtered for my_verisure
tail -f /config/home-assistant.log | grep my_verisure

# All logs
tail -f /config/home-assistant.log

# From Docker (outside container)
docker logs -f homeassistant
```

### Debug with Breakpoints

1. Set breakpoints in Python files
2. Press `F5` or Run → Start Debugging
3. Select "Home Assistant (DevContainer)"
4. Code execution pauses at breakpoints

### Test Services

From **Developer Tools → Services**:

```yaml
service: my_verisure.arm_away
data:
  installation_id: "YOUR_INSTALLATION_ID"
```

Or run a script:

```yaml
service: script.test_arm_away
```

### Check Configuration

```bash
# Validate HA configuration
container check-config

# Check for integration errors
grep -i error /config/home-assistant.log | grep my_verisure
```

## Customization

### Change Home Assistant Port

Edit `devcontainer.json`:

```json
"appPort": [
  "7124:8123"  // Use port 7124 instead
],
```

### Add More Extensions

Edit `devcontainer.json`:

```json
"extensions": [
  "ms-python.python",
  "your-extension-id"
]
```

### Adjust Log Levels

Edit `configuration.yaml`:

```yaml
logger:
  default: warning  # Less verbose
  logs:
    custom_components.my_verisure: debug
    homeassistant.components.alarm_control_panel: debug
```

### Install Additional Dependencies

In the container terminal:

```bash
pip install your-package
```

To persist, add to `custom_components/my_verisure/manifest.json`:

```json
"requirements": [
  "aiohttp>=3.8.0",
  "your-package>=1.0.0"
]
```

## Container Commands

Available in the container terminal:

```bash
container start        # Start Home Assistant
container restart      # Restart Home Assistant
container stop         # Stop Home Assistant
container check-config # Validate configuration
container logs         # Show logs
container set-owner    # Fix file permissions
```

## Troubleshooting

### Container Won't Start

```bash
# Rebuild container
# In Cursor/VS Code: Cmd+Shift+P → Remote-Containers: Rebuild Container

# Or manually remove and rebuild
docker stop homeassistant
docker rm homeassistant
# Then reopen in container
```

### Integration Not Loading

1. **Check manifest.json:**
   ```bash
   cat /workspaces/core/config/custom_components/my_verisure/manifest.json
   ```

2. **Verify mount:**
   ```bash
   ls -la /workspaces/core/config/custom_components/my_verisure
   ```

3. **Check logs:**
   ```bash
   grep -i "my_verisure" /config/home-assistant.log | grep -i error
   ```

### Port Already in Use

If port 7123 is in use:

1. Find and stop the process using the port
2. Or change the port in `devcontainer.json`

### Changes Not Reflecting

- **Integration changes:** Restart HA with `container restart`
- **Config changes:** Reload YAML from Developer Tools
- **Entity changes:** May need full restart

### Slow Performance

The DevContainer runs a full Home Assistant instance. For better performance:

- Close unnecessary Cursor/VS Code extensions
- Allocate more resources to Docker Desktop (Preferences → Resources)
- Use Docker's built-in resource settings
- For Cursor: Disable AI features temporarily if needed (Settings → Cursor)

### File Permission Issues

```bash
# Fix ownership
container set-owner

# Or manually
sudo chown -R vscode:vscode /workspaces
```

## Alternative Approaches

If DevContainer doesn't work for you:

### Standalone Docker

```bash
./dev docker-start  # Uses helper script
# Or manually: see docs/developer-guide/local-development.md
```

### Python Virtual Environment

```bash
./dev setup
source venv/bin/activate
# See docs/developer-guide/local-development.md
```

## Resources

- **Official HA DevContainer docs:** https://developers.home-assistant.io/docs/development_environment
- **VS Code DevContainers:** https://code.visualstudio.com/docs/remote/containers
- **Cursor Documentation:** https://docs.cursor.sh
- **Project docs:** [../docs/developer-guide/local-development.md](../docs/developer-guide/local-development.md)

## Cursor-Specific Notes

Cursor is built on VS Code's foundation, so:
- ✅ All DevContainer features work identically
- ✅ Same keyboard shortcuts (`Cmd+Shift+P`, `F5`, etc.)
- ✅ Same extensions (Python, Pylance, etc.)
- ✅ Debugging works the same way
- ✅ Tasks and launch configurations are compatible
- 🎁 **Bonus:** You get Cursor's AI features inside the container!

## Notes

- The container uses **Home Assistant Core** (not Supervisor/OS)
- SQLite database is in `/tmp` and cleared on container restart (intentional for testing)
- Integration code is **live-mounted** (no copy, direct edits)
- Container state persists between VS Code sessions
- Logs are in `/config/home-assistant.log`
