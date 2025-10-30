from icontract import require, ensure

@require(lambda title: isinstance(title, str))
@require(lambda title: 1 <= len(title.strip()) <= 40)
@ensure(lambda title, result: result == title.strip())
def normalize_title(title: str) -> str:
    """Titles must be 1..40 chars after trim; function returns the normalized title."""
    return title.strip()
