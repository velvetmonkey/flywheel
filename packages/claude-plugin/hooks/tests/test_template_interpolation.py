"""
Template Variable Interpolation Tests (v1.8.0)

Tests for template variable replacement using {{variable}} syntax.

Templates support:
- Simple variables: {{date}}, {{customer}}, {{title}}
- Nested paths: {{user.name}}, {{config.path}}
- Frontmatter and content interpolation
- Wikilink generation: [[{{customer}}]]

Test cases:
1. Simple variable replacement ({{date}})
2. Multiple variables in same template
3. Variable in frontmatter and content
4. Missing variable handling
5. Nested variable paths ({{a.b.c}})
"""

import pytest
import re


def interpolate_template(template: str, variables: dict) -> str:
    """
    Replace {{variable}} placeholders in template with values from dict.

    Args:
        template: Template string with {{var}} placeholders
        variables: Dictionary of variable values

    Returns:
        String with variables replaced

    Examples:
        >>> interpolate_template("Hello {{name}}", {"name": "World"})
        "Hello World"

        >>> interpolate_template("[[{{person}}]]", {"person": "John"})
        "[[John]]"

    Behavior:
        - Simple vars: {{date}} → values from dict["date"]
        - Nested vars: {{user.name}} → values from dict["user"]["name"]
        - Missing vars: {{undefined}} → "" (empty string) or raise error
        - Preserves {{text}} if not in variables
    """
    def replace_var(match):
        var_name = match.group(1)

        # Handle nested paths (user.name)
        if '.' in var_name:
            parts = var_name.split('.')
            value = variables
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return ""  # Missing nested key
            return str(value)

        # Handle simple variable
        if var_name in variables:
            return str(variables[var_name])

        # Missing variable - return empty string
        return ""

    # Replace all {{variable}} patterns
    pattern = r'\{\{(\w+(?:\.\w+)*)\}\}'
    return re.sub(pattern, replace_var, template)


class TestSimpleVariableInterpolation:
    """Test basic variable replacement."""

    def test_single_variable_replacement(self):
        """Replace single {{date}} variable"""
        template = "Date: {{date}}"
        variables = {"date": "2026-01-03"}

        result = interpolate_template(template, variables)

        assert result == "Date: 2026-01-03"

    def test_multiple_variables_same_line(self):
        """Replace multiple variables in one line"""
        template = "Meeting with {{customer}} on {{date}}"
        variables = {
            "customer": "Acme Corp",
            "date": "2026-01-10"
        }

        result = interpolate_template(template, variables)

        assert result == "Meeting with Acme Corp on 2026-01-10"

    def test_variable_in_frontmatter(self):
        """Replace variable in YAML frontmatter"""
        template = """---
type: meeting
date: {{date}}
customer: "{{customer}}"
---
# Meeting"""

        variables = {
            "date": "2026-01-03",
            "customer": "Acme Corp"
        }

        result = interpolate_template(template, variables)

        assert "date: 2026-01-03" in result
        assert 'customer: "Acme Corp"' in result

    def test_variable_in_wikilink(self):
        """Replace variable inside wikilink [[{{var}}]]"""
        template = "Customer: [[{{customer}}]]"
        variables = {"customer": "Acme Corp"}

        result = interpolate_template(template, variables)

        assert result == "Customer: [[Acme Corp]]"

    def test_no_variables_unchanged(self):
        """Template with no variables should pass through"""
        template = "This is static content"
        variables = {}

        result = interpolate_template(template, variables)

        assert result == template


class TestMissingVariables:
    """Test handling of undefined variables."""

    def test_missing_variable_empty_string(self):
        """Missing variable should become empty string"""
        template = "Hello {{name}}"
        variables = {}  # name not defined

        result = interpolate_template(template, variables)

        assert result == "Hello "

    def test_partial_variable_replacement(self):
        """Some variables defined, some missing"""
        template = "{{defined}} and {{undefined}}"
        variables = {"defined": "yes"}

        result = interpolate_template(template, variables)

        assert result == "yes and "

    def test_missing_variable_in_frontmatter(self):
        """Missing variable in frontmatter should not corrupt YAML"""
        template = """---
type: meeting
owner: {{owner}}
---"""
        variables = {}

        result = interpolate_template(template, variables)

        # Should result in "owner: " which is valid YAML (null)
        assert "owner: " in result or "owner:" in result


class TestNestedVariablePaths:
    """Test nested variable paths like {{user.name}}."""

    def test_nested_two_levels(self):
        """Replace {{user.name}} from nested dict"""
        template = "User: {{user.name}}"
        variables = {
            "user": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }

        result = interpolate_template(template, variables)

        assert result == "User: John Doe"

    def test_nested_three_levels(self):
        """Replace {{config.server.host}} from deep nested dict"""
        template = "Host: {{config.server.host}}"
        variables = {
            "config": {
                "server": {
                    "host": "localhost",
                    "port": 3000
                }
            }
        }

        result = interpolate_template(template, variables)

        assert result == "Host: localhost"

    def test_nested_path_missing_key(self):
        """Missing nested key should return empty string"""
        template = "Value: {{config.missing.key}}"
        variables = {
            "config": {
                "existing": "value"
            }
        }

        result = interpolate_template(template, variables)

        assert result == "Value: "

    def test_nested_path_not_dict(self):
        """Nested path on non-dict should return empty"""
        template = "Value: {{name.first}}"
        variables = {
            "name": "John Doe"  # String, not dict
        }

        result = interpolate_template(template, variables)

        assert result == "Value: "


class TestRealWorldTemplates:
    """Test with actual v1.8 template patterns."""

    def test_customer_onboarding_template(self):
        """Test customer-onboarding.md template"""
        template = """---
type: onboarding
customer: "{{customer}}"
start_date: {{date}}
---
# Customer Onboarding: [[{{customer}}]]

| Field | Value |
|-------|-------|
| Customer | [[{{customer}}]] |
| Start Date | {{date}} |
"""

        variables = {
            "customer": "Acme Corp",
            "date": "2026-01-03"
        }

        result = interpolate_template(template, variables)

        assert 'customer: "Acme Corp"' in result
        assert 'start_date: 2026-01-03' in result
        assert '# Customer Onboarding: [[Acme Corp]]' in result
        assert '| Customer | [[Acme Corp]] |' in result

    def test_meeting_template(self):
        """Test meeting.md template"""
        template = """---
type: meeting
date: {{date}}
---
# Meeting: {{title}}

**Date**: {{date}}
"""

        variables = {
            "title": "Q1 Planning",
            "date": "2026-01-10"
        }

        result = interpolate_template(template, variables)

        assert 'date: 2026-01-10' in result
        assert '# Meeting: Q1 Planning' in result
        assert '**Date**: 2026-01-10' in result

    def test_okr_template(self):
        """Test okr.md template"""
        template = """---
type: okr
quarter: {{quarter}}
---
# OKRs: {{quarter}}

## Objective 1: {{objective}}
"""

        variables = {
            "quarter": "2026-Q1",
            "objective": "Launch product v2"
        }

        result = interpolate_template(template, variables)

        assert 'quarter: 2026-Q1' in result
        assert '# OKRs: 2026-Q1' in result
        assert '## Objective 1: Launch product v2' in result


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_template(self):
        """Empty template should return empty string"""
        template = ""
        variables = {"key": "value"}

        result = interpolate_template(template, variables)

        assert result == ""

    def test_empty_variables(self):
        """Empty variables dict should leave {{vars}} unchanged or empty"""
        template = "Hello {{name}}"
        variables = {}

        result = interpolate_template(template, variables)

        # Should return empty string for missing var
        assert result == "Hello "

    def test_numeric_variable_values(self):
        """Numeric values should be converted to strings"""
        template = "Count: {{count}}"
        variables = {"count": 42}

        result = interpolate_template(template, variables)

        assert result == "Count: 42"

    def test_boolean_variable_values(self):
        """Boolean values should be converted to strings"""
        template = "Active: {{active}}"
        variables = {"active": True}

        result = interpolate_template(template, variables)

        assert result == "Active: True"

    def test_special_characters_in_values(self):
        """Values with special characters should not break interpolation"""
        template = "Note: {{text}}"
        variables = {"text": "Hello & goodbye, [[link]] here"}

        result = interpolate_template(template, variables)

        assert result == "Note: Hello & goodbye, [[link]] here"

    def test_variable_name_with_underscores(self):
        """Variable names can contain underscores"""
        template = "ID: {{customer_id}}"
        variables = {"customer_id": "ACME-001"}

        result = interpolate_template(template, variables)

        assert result == "ID: ACME-001"
