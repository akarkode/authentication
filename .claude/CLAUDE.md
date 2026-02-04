# Code Style Rules

## Naming Conventions
- Use snake_case for variables and functions
- Use PascalCase for classes
- Use SCREAMING_SNAKE_CASE for constants

## Code Formatting
- No comments in code
- No inline documentation
- Minimal whitespace
- 2-space indentation

## Response Style
- Provide executable code only
- No explanations unless asked
- Choose best solution, no options

## Type Hints
- Always use type hints for parameters and return values
- Use typing module for complex types (List, Dict, Optional, Union, Callable)
- Type hints must be clear and specific, never use Any unnecessarily

## Error Handling
- Use specific exceptions, never bare except
- Catch only exceptions that can be handled
- No silent failures, always log or raise errors
- Validate input at system boundaries

## Security Requirements
- No hardcoded credentials, secrets, or API keys
- Validate and sanitize all user input
- Use parameterized queries for database operations
- Sanitize output to prevent XSS and injection attacks
- Never use eval() or unsafe deserialization

## API Testing Requirements
- Every endpoint must have corresponding tests
- Never auto-generate tests without explicit request
- Verify test coverage before completion
- Tests must cover both success and error paths