# Claude Code Configuration Guide

This document explains how the `.claude/config.json` file works and how to optimize it for your project.

## Overview

The `config.json` file tells Claude Code about your project structure, preferences, and conventions. This helps Claude provide better, more context-aware assistance.

---

## Configuration Sections

### 1. Model Configuration

```json
{
  "model": {
    "default": "claude-sonnet-4-20250514",
    "temperature": 0.7
  }
}
```

**How it works:**
- `default` - Specifies which Claude model to use
  - `claude-sonnet-4-20250514` - Balanced performance and speed (recommended)
  - `claude-opus-4-5-20251101` - Most capable but slower
  - `claude-haiku-...` - Fastest but less capable
- `temperature` - Controls randomness (0.0-1.0)
  - `0.7` - Good balance for code generation
  - Lower = more deterministic, Higher = more creative

**When to change:**
- Use Opus for complex architectural decisions
- Use Haiku for simple, repetitive tasks
- Adjust temperature lower (0.3-0.5) for more predictable code

---

### 2. Project Configuration

```json
{
  "project": {
    "name": "Authentication Service",
    "type": "python",
    "framework": "fastapi",
    "description": "...",
    "python_version": "3.12",
    "package_manager": "poetry"
  }
}
```

**How it works:**
- Claude uses this to understand your tech stack
- Affects code suggestions, error detection, and best practices
- `type` and `framework` help Claude provide framework-specific advice

**Project Commands:**
```json
{
  "test_command": "poetry run pytest -v --cov=app",
  "dev_server": "poetry run uvicorn main:app --reload",
  "migration_create": "poetry run alembic revision --autogenerate -m"
}
```

**How it works:**
- Claude can run these commands when you ask to test, run, or migrate
- Commands are executed exactly as specified
- Use full commands including `poetry run` for consistency

**Why this helps:**
- ✅ "Run the tests" → Claude knows to use `poetry run pytest -v --cov=app`
- ✅ "Start the server" → Claude runs the exact dev server command
- ✅ "Create a migration" → Claude uses the right migration command

---

### 3. Context Configuration

This is **the most important section** for performance and relevance.

```json
{
  "context": {
    "include_patterns": [
      "app/**/*.py",
      "tests/**/*.py",
      "*.md"
    ],
    "exclude_patterns": [
      "__pycache__/**",
      "*.pyc",
      "poetry.lock"
    ],
    "max_file_size_kb": 500,
    "follow_symlinks": false
  }
}
```

**How it works:**

#### Include Patterns
- Defines which files Claude should pay attention to
- Uses glob patterns:
  - `**/*.py` - All Python files in any subdirectory
  - `app/**/*.py` - Only Python files in app directory
  - `*.md` - Markdown files in root only
  - `*.toml` - Config files like pyproject.toml

**Our include patterns explained:**
- `app/**/*.py` - All application code
- `tests/**/*.py` - All test code
- `alembic/versions/*.py` - Migration files (important for DB changes)
- `*.py` - Root Python files (main.py)
- `*.md`, `*.toml`, `*.ini` - Configuration and documentation
- `.env.example` - Template for environment variables
- `Dockerfile`, `.dockerignore` - Container configuration

#### Exclude Patterns
- Tells Claude which files to ignore
- Reduces context size and improves speed
- Prevents Claude from reading irrelevant files

**Our exclude patterns explained:**
- `__pycache__/**`, `*.pyc`, `*.pyo` - Python bytecode (generated)
- `.venv/**`, `venv/**` - Virtual environment (huge, not needed)
- `poetry.lock` - Lock file (92KB, auto-generated)
- `.pytest_cache/**`, `.coverage` - Test artifacts
- `*.db`, `*.sqlite*` - Database files
- `.git/**` - Git internals (not needed)

**Performance impact:**
```
Without excludes: Claude reads 1000+ files including venv
With excludes: Claude reads ~50 relevant files
Result: 20x faster context loading, more accurate responses
```

#### Max File Size
- `max_file_size_kb: 500` - Skip files larger than 500KB
- Prevents Claude from reading huge generated files
- Saves tokens and improves response speed

---

### 4. Testing Configuration

```json
{
  "testing": {
    "framework": "pytest",
    "async_mode": "auto",
    "coverage_threshold": 80,
    "markers": {
      "unit": "Fast unit tests",
      "integration": "Integration tests"
    }
  }
}
```

**How it works:**
- Claude understands your testing setup
- Helps write tests that match your conventions
- Knows about test markers and coverage requirements

**Why this helps:**
- ✅ "Write a test for this function" → Claude writes pytest-compatible tests
- ✅ "Run unit tests" → Claude uses `-m unit` marker
- ✅ Claude suggests async test patterns automatically

---

### 5. Development Configuration

```json
{
  "development": {
    "auto_reload": true,
    "debug": false,
    "port": 8000,
    "host": "0.0.0.0"
  }
}
```

**How it works:**
- Defines default development server settings
- Used when Claude starts or configures the dev server
- Ensures consistency across development

---

### 6. Architecture Configuration

```json
{
  "architecture": {
    "patterns": [
      "Repository pattern (CRUD)",
      "Dependency injection",
      "OAuth 2.0 flow"
    ],
    "key_directories": {
      "app/src/core": "Configuration and security",
      "app/src/models": "SQLAlchemy models"
    },
    "conventions": {
      "imports": "Use 'from __future__ import annotations'",
      "async": "All database operations use async/await"
    }
  }
}
```

**How it works:**
- Documents your project's architecture
- Claude follows these patterns when writing code
- Helps maintain consistency across the codebase

**Real examples:**
- ✅ "Add a new CRUD operation" → Claude follows repository pattern
- ✅ "Create a new endpoint" → Claude uses dependency injection
- ✅ "Add a database query" → Claude writes async code

**Why this helps:**
- New code matches existing patterns
- No need to explain patterns repeatedly
- Better code consistency

---

### 7. Dependencies Configuration

```json
{
  "dependencies": {
    "production": ["fastapi", "sqlalchemy", "pyjwt"],
    "dev": ["pytest", "pytest-asyncio"]
  }
}
```

**How it works:**
- Claude knows which packages are available
- Prevents suggestions to install packages you already have
- Helps distinguish between prod and dev dependencies

**Why this helps:**
- ✅ Claude won't suggest installing fastapi (already there)
- ✅ Claude knows pytest is available for testing
- ✅ Claude suggests appropriate packages for new features

---

### 8. AI Instructions

```json
{
  "ai_instructions": {
    "code_style": "Follow PEP 8, use type hints",
    "testing": "Write tests for new features, aim for 80%+ coverage",
    "security": "Never commit secrets, validate all inputs",
    "git": "Use conventional commits with emojis",
    "documentation": "Add docstrings for complex functions"
  }
}
```

**How it works:**
- Direct instructions for Claude's behavior
- Enforces project-specific rules
- Complements your team's coding standards

**Real impact:**
- ✅ Claude adds type hints automatically
- ✅ Claude suggests writing tests after creating features
- ✅ Claude validates user inputs in new endpoints
- ✅ Claude creates proper commit messages

---

## Best Practices

### 1. Keep Include Patterns Specific
```json
// ❌ Too broad
"include_patterns": ["**/*"]

// ✅ Specific
"include_patterns": ["app/**/*.py", "tests/**/*.py"]
```

### 2. Exclude Generated Files
```json
"exclude_patterns": [
  "poetry.lock",      // Auto-generated
  "__pycache__/**",   // Compiled Python
  "*.db",             // Database files
  ".venv/**"          // Virtual environment
]
```

### 3. Document Your Architecture
```json
// ✅ Good - Explains patterns
"patterns": [
  "Repository pattern (CRUD)",
  "JWT authentication with access/refresh tokens"
]

// ❌ Bad - Too vague
"patterns": ["Clean architecture"]
```

### 4. Set Realistic Coverage Goals
```json
"coverage_threshold": 80  // ✅ Achievable goal
"coverage_threshold": 100 // ❌ Usually unrealistic
```

---

## Performance Tips

### Token Usage Optimization

**Problem:** Large context = more tokens = slower responses

**Solutions:**

1. **Exclude lock files:**
   ```json
   "exclude_patterns": ["poetry.lock", "package-lock.json"]
   ```
   Saves: ~2000-5000 tokens per request

2. **Limit file size:**
   ```json
   "max_file_size_kb": 500
   ```
   Prevents reading huge generated files

3. **Specific includes:**
   ```json
   "include_patterns": ["app/**/*.py"]  // Only app code
   ```
   Instead of:
   ```json
   "include_patterns": ["**/*.py"]  // Everything
   ```

### Speed Optimization

**Choose the right model:**
- Fast queries → `"default": "claude-haiku-..."`
- Balanced → `"default": "claude-sonnet-4-20250514"`
- Complex tasks → `"default": "claude-opus-4-5-20251101"`

---

## Common Issues

### Issue 1: Claude Reads Too Many Files

**Symptom:** Slow responses, high token usage

**Solution:**
```json
"exclude_patterns": [
  ".venv/**",
  "node_modules/**",
  "*.lock",
  ".git/**"
]
```

### Issue 2: Claude Doesn't See Important Files

**Symptom:** Claude says "I can't find that file"

**Solution:**
```json
"include_patterns": [
  "app/**/*.py",     // Add missing directories
  "scripts/**/*.sh"
]
```

### Issue 3: Claude Suggests Wrong Patterns

**Symptom:** Code doesn't match your architecture

**Solution:**
```json
"architecture": {
  "patterns": ["Specify your exact patterns here"],
  "conventions": {
    "routing": "API versioning via /v1, /v2 prefixes"
  }
}
```

---

## Testing Your Configuration

### 1. Verify Include/Exclude Patterns

Ask Claude:
- "What files can you see in the app directory?"
- "List all Python files you have access to"

### 2. Test Commands

Ask Claude:
- "Run the tests"
- "Start the development server"

Claude should use your configured commands.

### 3. Check Architecture Understanding

Ask Claude:
- "What architecture patterns does this project use?"
- "How should I create a new CRUD operation?"

Claude should reference your architecture settings.

---

## Updating the Config

### When to Update

1. **New dependencies added:**
   ```json
   "dependencies": {
     "production": ["fastapi", "new-package"]
   }
   ```

2. **Architecture changes:**
   ```json
   "patterns": ["Add new pattern"]
   ```

3. **New directories:**
   ```json
   "include_patterns": ["new_module/**/*.py"]
   ```

### How to Update

1. Edit `.claude/config.json`
2. Save the file
3. Claude automatically picks up changes
4. No restart required

---

## Example Workflow

**Without config.json:**
```
You: "Run the tests"
Claude: "What test framework do you use? What's the command?"
You: "pytest with poetry"
Claude: "Ok, running poetry run pytest"
```

**With config.json:**
```
You: "Run the tests"
Claude: *Runs poetry run pytest -v --cov=app*
Claude: "All tests passed! Coverage: 85%"
```

**Saved:** 2-3 back-and-forth messages per interaction

---

## Summary

The `config.json` file:
- ✅ Speeds up Claude's responses (excludes unnecessary files)
- ✅ Improves code quality (follows your patterns)
- ✅ Reduces repetition (remembers commands and conventions)
- ✅ Maintains consistency (enforces architecture rules)

**ROI:** 5 minutes to configure = hours saved in explanations
