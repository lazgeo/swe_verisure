# Using DevContainer with Cursor

This project's DevContainer works perfectly with **Cursor**! Since Cursor is built on VS Code, all DevContainer functionality is 100% compatible.

## Quick Start

```bash
# Open the project
cursor .

# Cursor will detect .devcontainer and prompt: "Reopen in Container"
# Click it!

# Wait for container to build (~5 minutes first time)

# Start Home Assistant
container start

# Access at http://localhost:7123
```

## What Works in Cursor

✅ **Everything from VS Code:**
- DevContainer detection and setup
- Remote container connection
- Port forwarding (you'll see port 7123 forwarded)
- Terminal access inside the container
- File editing with live sync
- All extensions (Python, Pylance, Black, etc.)
- Debugging with breakpoints
- Tasks (Cmd+Shift+P → Tasks: Run Task)
- Integrated Git

✅ **Plus Cursor-specific features:**
- AI Chat works inside the container
- AI Cmd+K (inline editing) works
- AI code completions work
- All Cursor features available

## Keyboard Shortcuts

Same as VS Code:
- `Cmd+Shift+P` (Mac) / `Ctrl+Shift+P` (Windows/Linux) - Command palette
- `F5` - Start debugging
- `Cmd+~` - Toggle terminal
- `Cmd+B` - Toggle sidebar

## Common Tasks

### Start Home Assistant
```bash
# In terminal (inside container)
container start
```

Or: `Cmd+Shift+P` → **Tasks: Run Task** → **Run Home Assistant**

### Restart After Changes
```bash
container restart
```

Or: `Cmd+Shift+P` → **Tasks: Run Task** → **Restart Home Assistant**

### View Logs
```bash
tail -f /config/home-assistant.log | grep my_verisure
```

### Debug with Breakpoints
1. Click in the gutter to add a breakpoint
2. Press `F5`
3. Select **Home Assistant (DevContainer)**
4. Code pauses at breakpoint - inspect variables!

### Run Tests
```bash
pytest custom_components/my_verisure/tests/ -v
```

Or: `Cmd+Shift+P` → **Tasks: Run Task** → **Run Tests**

## Cursor AI Features in DevContainer

### AI Chat
- Open chat with `Cmd+L` (Mac) / `Ctrl+L` (Windows/Linux)
- Ask questions about the code
- Works with files inside the container!

Example prompts:
```
"Explain how the coordinator updates data"
"Find where the alarm states are defined"
"How does the config flow handle OTP?"
```

### AI Cmd+K (Inline Editing)
- Select code
- Press `Cmd+K` (Mac) / `Ctrl+K` (Windows/Linux)
- Give instruction
- AI edits the code inline

Example:
1. Select a function
2. `Cmd+K`
3. "Add error handling for network failures"
4. AI rewrites the function

### AI Autocomplete
- Type as normal
- Cursor suggests completions
- Press `Tab` to accept

## Port Forwarding

Cursor automatically forwards port 7123. Check the **Ports** panel:

1. Click on the "Ports" tab (bottom panel)
2. You should see: `7123` → `8123`
3. Click the globe icon to open in browser

## Tips for Cursor Users

### 1. Use AI to Understand HA Code
```
Ask in chat:
"What does DataUpdateCoordinator do in Home Assistant?"
"Explain the entity platform setup flow"
"How do config entries work?"
```

### 2. Generate Tests with AI
```
Select a function, Cmd+K:
"Generate a pytest test for this function with mocks"
```

### 3. Quick Refactoring
```
Select code, Cmd+K:
"Extract this into a separate helper function"
"Add type hints to all parameters"
"Make this async"
```

### 4. Documentation
```
Select a function, Cmd+K:
"Add a Google-style docstring"
```

## Troubleshooting

### Cursor Doesn't Detect DevContainer

1. Make sure you're in the project root
2. Check `.devcontainer/devcontainer.json` exists
3. Reload window: `Cmd+Shift+P` → **Developer: Reload Window**

### Can't Connect to Container

1. Check Docker Desktop is running
2. Try: `Cmd+Shift+P` → **Remote-Containers: Rebuild Container**
3. Check Docker logs: `docker logs homeassistant`

### Extensions Not Loading

The container should auto-install these extensions:
- `ms-python.python`
- `ms-python.vscode-pylance`
- `ms-python.black-formatter`
- `redhat.vscode-yaml`

If missing, install manually:
1. Open Extensions panel
2. Search for extension
3. Click **Install in Container**

### AI Features Not Working

Cursor AI features should work inside containers. If not:
1. Check your Cursor subscription is active
2. Try: `Cmd+Shift+P` → **Cursor: Restart Extension Host**
3. Check network connection

### Port 7123 Not Accessible

1. Check the **Ports** panel (bottom)
2. Verify 7123 is listed
3. Try clicking the globe icon to open
4. Try manually: http://localhost:7123
5. Alternative: http://127.0.0.1:7123

## Performance Tips

DevContainer + Cursor can be resource-intensive:

1. **Close unused files** - Reduces memory usage
2. **Disable AI temporarily** - Settings → Cursor → Disable for heavy debugging
3. **Allocate more RAM to Docker** - Docker Desktop → Preferences → Resources
4. **Use selective indexing** - Cursor only indexes what you need

## Differences from VS Code

**Almost none!** But here are subtle differences:

| Feature | Cursor | VS Code |
|---------|--------|---------|
| DevContainer support | ✅ Same | ✅ Same |
| Extensions | ✅ Compatible | ✅ Native |
| Debugging | ✅ Same | ✅ Same |
| Tasks | ✅ Same | ✅ Same |
| AI Features | ✅ Built-in | ❌ Needs Copilot |
| Settings | ✅ Shared | ✅ Standard |

## Resources

- **Cursor Docs:** https://docs.cursor.sh
- **VS Code DevContainers:** https://code.visualstudio.com/docs/remote/containers
- **Project Guide:** [local-development.md](../docs/developer-guide/local-development.md)
- **Home Assistant Dev Docs:** https://developers.home-assistant.io

## Example Workflow

Here's a typical development session in Cursor:

```bash
# 1. Open project in container
cursor .
# Click "Reopen in Container"

# 2. Start HA
container start

# 3. Make a change
# Edit custom_components/my_verisure/sensor.py

# 4. Use AI to help
# Cmd+L: "How should I structure this sensor class?"

# 5. Add a feature
# Cmd+K: "Add a new sensor for alarm battery level"

# 6. Test it
pytest custom_components/my_verisure/tests/test_sensor.py -v

# 7. Restart HA to see changes
container restart

# 8. Check in browser
# http://localhost:7123

# 9. Debug if needed
# Add breakpoint, press F5

# 10. Use AI to review
# Cmd+L: "Review this code for potential issues"
```

## Need Help?

- **Cursor Questions:** Ask in Cursor's chat with `Cmd+L`
- **Project Questions:** See [local-development.md](../docs/developer-guide/local-development.md)
- **Home Assistant Questions:** https://developers.home-assistant.io/docs

---

**Enjoy developing with Cursor + DevContainer! 🎉**
