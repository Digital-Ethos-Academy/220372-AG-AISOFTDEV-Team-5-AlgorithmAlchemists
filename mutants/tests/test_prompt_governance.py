import re

def test_prompts_version_and_return_json():
    with open("prompts.md", "r", encoding="utf-8") as f:
        content = f.read()
    # Extract numbered prompt sections
    sections = re.split(r"^## \\d+\. ", content, flags=re.MULTILINE)[1:]
    assert sections, "No prompt sections found"
    for sec in sections:
        # Ensure version pattern (vX.Y)
        assert re.search(r"\(v\d+\.\d+\)", sec), "Missing version tag in a prompt section"
        # Ensure 'Return JSON' guidance present
        assert "Return JSON" in sec or "Return Markdown" in sec, "Missing output format directive"
