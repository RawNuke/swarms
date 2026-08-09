from swarms.utils.formatter import (
    Formatter,
    MarkdownOutputHandler,
)


def test_formatter():
    """Test the formatter with various markdown content."""
    formatter = Formatter(md=True)

    # Test 1: Basic markdown with headers
    content1 = """# Main Title

This is a paragraph with **bold** text and *italic* text.

## Section 1
- Item 1
- Item 2
- Item 3

### Subsection
This is another paragraph with `inline code`.
"""

    formatter.print_panel(
        content1, title="Test 1: Basic Markdown", style="bold blue"
    )

    # Test 2: Code blocks with syntax highlighting
    content2 = """## Code Examples

Here's a Python example:

```python
def hello_world():
    '''A simple hello world function.'''
    print("Hello, World!")
    return True
```

And here's some JavaScript:

```javascript
function greet(name) {
    console.log(`Hello, ${name}!`);
}
```

Plain text code block:

```
This is just plain text
without any syntax highlighting
```
"""

    formatter.print_panel(
        content2, title="Test 2: Code Blocks", style="bold green"
    )

    # Test 3: Mixed content
    content3 = """## Mixed Content Test

This paragraph includes **various** formatting options:
- Lists with `code`
- Links [like this](https://example.com)
- And more...

```python
# Python code with comments
class Example:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!"
```

### Table Example

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
"""

    formatter.print_panel(
        content3, title="Test 3: Mixed Content", style="bold magenta"
    )

    # Test 4: Edge cases
    content4 = """This content starts without a header

It should still be formatted correctly.

```
No language specified
```

Single line content."""

    formatter.print_panel(
        content4, title="Test 4: Edge Cases", style="bold yellow"
    )

    # Test 5: Empty content
    formatter.print_panel(
        "", title="Test 5: Empty Content", style="bold red"
    )

    # Test 6: Using print_markdown method
    content6 = """# Direct Markdown Rendering

This uses the `print_markdown` method directly.

```python
# Syntax highlighted code
result = 42 * 2
print(f"The answer is {result}")
```
"""

    formatter.print_markdown(
        content6, title="Test 6: Direct Markdown", border_style="cyan"
    )


def test_clean_output_strips_every_log_level():
    """_clean_output must strip every loguru log level from the
    output."""
    from rich.console import Console

    console = Console()
    handler = MarkdownOutputHandler(console)

    log_levels = [
        "INFO",
        "DEBUG",
        "WARNING",
        "ERROR",
        "SUCCESS",
        "TRACE",
        "CRITICAL",
    ]

    for level in log_levels:
        log_line = (
            f"2026-01-01 12:00:00 | {level} | module:func | "
            f"Task completed successfully"
        )
        cleaned = handler._clean_output(log_line)
        assert (
            "2026-01-01" not in cleaned
        ), f"Timestamp not stripped for {level}: {cleaned}"
        assert (
            "Task completed successfully" in cleaned
        ), f"Message lost for {level}: {cleaned}"

    for level in log_levels:
        log_line = (
            f"{level} | module:func | extra:col | "
            f"Task completed"
        )
        cleaned = handler._clean_output(log_line)
        assert (
            "Task completed" in cleaned
        ), f"Message lost for {level}: {cleaned}"


def test_clean_output_handles_empty_string():
    """_clean_output must return an empty string for empty input."""
    from rich.console import Console

    console = Console()
    handler = MarkdownOutputHandler(console)
    assert handler._clean_output("") == ""


def test_clean_output_preserves_plain_text():
    """_clean_output must not modify text without log patterns."""
    from rich.console import Console

    console = Console()
    handler = MarkdownOutputHandler(console)
    text = "This is plain text without any log patterns."
    cleaned = handler._clean_output(text)
    assert "plain text" in cleaned


def test_dead_print_methods_are_removed():
    """The three dead print methods must not exist on Formatter."""
    formatter = Formatter(md=False)
    assert not hasattr(formatter, "print_progress")
    assert not hasattr(formatter, "print_panel_token_by_token")
    assert not hasattr(formatter, "print_plan_tree")


def test_print_markdown_still_works_as_alias():
    """print_markdown must still be callable and forward to
    print_panel."""
    formatter = Formatter(md=False)
    assert hasattr(formatter, "print_markdown")
    formatter.print_markdown("Hello", title="Alias Test")


if __name__ == "__main__":
    test_formatter()
