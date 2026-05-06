---
name: generate-readme
description: Genera documentación README comprehensiva para proyectos Python/Home Assistant
---

# Generate README

## Overview

Crea documentación README.md exhaustiva y profesional para proyectos Python, especialmente integraciones de Home Assistant.

**Announce at start:** "Estoy usando la skill generate-readme para crear documentación comprehensiva."

## README Structure

### 1. Header Section

```markdown
# [Project Name]

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](...)
[![version](https://img.shields.io/badge/version-1.0.0-blue.svg)](...)
[![python](https://img.shields.io/badge/python-3.11+-blue.svg)](...)

Una descripción concisa de 1-2 líneas de qué hace el proyecto.
```

### 2. Features Section

Lista características principales con emojis para escaneabilidad:

```markdown
## 🚀 Features

- ✅ **Feature 1**: Descripción breve
- ✅ **Feature 2**: Descripción breve
- ✅ **Feature 3**: Descripción breve
```

### 3. Requirements

```markdown
## 📋 Requirements

- Python 3.11 or higher
- Dependency 1
- Dependency 2
```

### 4. Installation

Múltiples opciones si aplica:

```markdown
## 🛠️ Installation

### Option 1: HACS (Recommended)

1. Step 1
2. Step 2
3. Step 3

### Option 2: Manual

1. Step 1
2. Step 2
```

### 5. Configuration

Con ejemplos concretos:

```markdown
## ⚙️ Configuration

Paso a paso con screenshots o code blocks:

\`\`\`yaml
# Example config
key: value
\`\`\`
```

### 6. Usage

Ejemplos prácticos:

```markdown
## 📖 Usage

### Basic Example

\`\`\`python
from my_project import Client

client = Client()
result = client.do_something()
\`\`\`

### Advanced Example

...
```

### 7. Available Entities/Services

Para integraciones de Home Assistant:

```markdown
## 🔧 Available Entities

### Alarm Control Panel
- **Entity ID**: `alarm_control_panel.my_verisure_alarm`
- **States**: `armed_away`, `armed_home`, `disarmed`
- **Services**: `arm_away`, `arm_home`, `disarm`

### Sensors
Lista de sensores con descripción
```

### 8. Development

```markdown
## 🛠️ Development

### Quick Setup

\`\`\`bash
# Clone
git clone ...

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest
\`\`\`

### Project Structure

\`\`\`
project/
├── src/
├── tests/
└── README.md
\`\`\`
```

### 9. Testing

Información sobre test suite:

```markdown
## 🧪 Testing

- **CLI Tests**: 92 tests
- **Core Tests**: 137 tests
- **Coverage**: 85%

\`\`\`bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src
\`\`\`
```

### 10. Contributing

```markdown
## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request
```

### 11. License & Support

```markdown
## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🆘 Support

- [Issues](https://github.com/user/repo/issues)
- [Discussions](https://github.com/user/repo/discussions)
```

## Content Guidelines

### Writing Style

1. **Conciso**: Una idea por párrafo
2. **Concreto**: Ejemplos reales, no placeholders
3. **Completo**: Toda la info necesaria para empezar
4. **Visual**: Usa emojis, code blocks, tablas

### What to Include

✅ **DO:**
- Comandos exactos que funcionen
- Ejemplos reales de código
- Troubleshooting común
- Screenshots si mejora comprensión
- Links a documentación adicional

❌ **DON'T:**
- Información obvia o redundante
- Ejemplos con "TODO" o "TBD"
- Información que se desactualiza rápido
- Exceso de badges innecesarios

## Process

1. **Explore**: Lee el proyecto completo
   - Código fuente
   - Tests
   - Configuración (manifest.json, setup.py, etc)
   - Documentación existente

2. **Outline**: Crea outline con secciones necesarias

3. **Write**: Escribe cada sección con ejemplos concretos

4. **Review**: Verifica:
   - ¿Puede un usuario nuevo configurarlo?
   - ¿Funcionan los comandos?
   - ¿Hay ejemplos claros?
   - ¿Está actualizado?

5. **Test**: Si es posible, ejecuta los comandos del README

## Integration with Other Skills

- Use **verification-before-completion** antes de finalizar
- Si generas plan de desarrollo, usa **writing-plans**
- Para arquitectura, considera **improve-codebase-architecture**

## Special Sections for Home Assistant

### Entity Documentation

```markdown
## 📊 Entity Guide

### alarm_control_panel.my_verisure_alarm

**Purpose**: Control de alarma principal

**States**:
- `disarmed`: Alarma desarmada
- `armed_away`: Armada modo ausente
- `armed_home`: Armada modo hogar

**Services**:
\`\`\`yaml
service: my_verisure.arm_away
data:
  installation_id: "123456"
\`\`\`

**Automation Example**:
\`\`\`yaml
automation:
  - alias: "Armar por la noche"
    trigger:
      platform: time
      at: "23:00:00"
    action:
      service: alarm_control_panel.alarm_arm_away
      target:
        entity_id: alarm_control_panel.my_verisure_alarm
\`\`\`
```

## Output

Guarda el README en la raíz del proyecto como `README.md`.

Si hay documentación adicional necesaria:
- `ENTITIES_GUIDE.md` - Guía detallada de entities
- `CONTRIBUTING.md` - Guía de contribución
- `CHANGELOG.md` - Historial de cambios
- `TROUBLESHOOTING.md` - Resolución de problemas

## Remember

- README es la primera impresión del proyecto
- Debe ser comprehensivo pero escaneable
- Ejemplos concretos > explicaciones abstractas
- Mantener actualizado con el código
