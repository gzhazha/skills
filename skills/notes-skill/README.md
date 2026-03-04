# notes-skill

Unified CLI for PDF-to-note conversion, knowledge base management, study planning, test generation, and weakness analysis.

## Quick Start

Install dependencies:

```bash
pip install -r /Users/guang/code/skills/skills/notes-skill/requirements.txt
```

Run CLI:

```bash
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill --help
```

## Common Commands

```bash
# Convert a PDF to markdown
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill convert-pdf ./lesson.pdf

# Convert PDF and add it into KB
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill add-pdf ./lesson.pdf --category python --title "Lesson 1" --tags intro,core

# Add existing markdown note into KB
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill add-note ./note.md --category python --title "My Note"

# List/search notes
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill list-notes
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill search python

# Update note content
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill update-note 1 --content "new content"

# Generate plan/test
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill generate-plan --duration 14 --focus python,algorithms --daily-hours 2.5
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill generate-test --topics python --difficulty medium --num-questions 10

# Analyze weakness
/Users/guang/code/skills/skills/notes-skill/scripts/notes-skill analyze-weakness --test-results ./graded_test.json
```
