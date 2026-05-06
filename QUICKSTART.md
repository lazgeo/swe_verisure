# Quick Start Guide

Get up and running with My Verisure development in 5 minutes!

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- [Cursor](https://cursor.sh) or [VS Code](https://code.visualstudio.com/) with [Remote Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## Setup (First Time)

```bash
# 1. Clone the repository
git clone <repository-url>
cd my_verisure

# 2. Open in Cursor (or VS Code)
cursor .
# Or: code .
```

Cursor/VS Code will detect the DevContainer and show a notification:
**"Reopen in Container"** → Click it!

⏱️ First time takes ~5 minutes (downloading Home Assistant image)

## Start Developing

Once the container is ready:

### 1. Start Home Assistant

Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux), then:
- Type: **Tasks: Run Task**
- Select: **Run Home Assistant**

Or in terminal:
```bash
container start
```

### 2. Open Home Assistant

Open your browser: **http://localhost:7123**

First time:
1. Create admin user
2. Set up your home location
3. Skip the initial setup
4. Go to **Settings → Devices & Services → Add Integration**
5. Search for "My Verisure"

### 3. Make Changes

1. Edit any file in `custom_components/my_verisure/`
2. Save (auto-formatted with Black)
3. Restart Home Assistant:
   - `Cmd+Shift+P` → **Tasks: Run Task** → **Restart Home Assistant**
   - Or from UI: **Developer Tools → YAML → Restart**

### 4. Debug with Breakpoints

1. Add a breakpoint (click line gutter)
2. Press `F5` or click **Run and Debug** (sidebar)
3. Select **Home Assistant (DevContainer)**
4. Code will pause at breakpoint!

## Common Tasks

```bash
# Run tests
pytest custom_components/my_verisure/tests/ -v

# Lint code
pylint custom_components/my_verisure

# Format code
black custom_components/my_verisure

# Check config
container check-config

# View logs
tail -f /config/home-assistant.log | grep my_verisure
```

## VS Code Tasks

Press `Cmd+Shift+P` → **Tasks: Run Task** → Select:

- **Run Home Assistant** - Start HA
- **Restart Home Assistant** - Restart after changes
- **Check Config** - Validate configuration
- **Run Tests** - Run pytest
- **Lint: Pylint** - Check code quality
- **Format: Black** - Auto-format code

## Test Services

1. Go to **Developer Tools → Services**
2. Select service (e.g., `my_verisure.arm_away`)
3. Add data:
   ```yaml
   installation_id: "YOUR_INSTALLATION_ID"
   ```
4. Click **Call Service**

## Check Entities

1. Go to **Developer Tools → States**
2. Search: "my_verisure"
3. View all entities and attributes

## Troubleshooting

### Container won't start
```bash
# Rebuild: Cmd+Shift+P → Remote-Containers: Rebuild Container
```

### Changes not showing
```bash
# Full restart
container restart
```

### Can't access http://localhost:7123
- Check Docker Desktop is running
- Verify port forwarding in Cursor/VS Code (Ports panel)
- Check logs: `docker logs homeassistant`
- Try: http://127.0.0.1:7123

### Integration not loading
```bash
# Check logs for errors
tail -f /config/home-assistant.log | grep -i error

# Verify integration is mounted
ls -la /config/custom_components/my_verisure
```

## Need More Help?

- **Full Guide:** [docs/developer-guide/local-development.md](docs/developer-guide/local-development.md)
- **Architecture:** [docs/developer-guide/architecture.md](docs/developer-guide/architecture.md)
- **Testing:** [docs/developer-guide/testing.md](docs/developer-guide/testing.md)
- **Contributing:** [docs/developer-guide/contributing.md](docs/developer-guide/contributing.md)

## Alternative Setups

Don't want to use DevContainer? See alternatives:

- **Docker only:** [docs/developer-guide/local-development.md#option-1-docker-container-no-devcontainer](docs/developer-guide/local-development.md#option-1-docker-container-no-devcontainer)
- **Python venv:** [docs/developer-guide/local-development.md#option-2-python-virtual-environment](docs/developer-guide/local-development.md#option-2-python-virtual-environment)

---

**Ready to contribute?** Read [Contributing Guide](docs/developer-guide/contributing.md)
