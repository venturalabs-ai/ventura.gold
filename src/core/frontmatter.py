"""
Frontmatter parser for venture.gold agents and skills.

Accepts simple frontmatter with: id, name, description, capabilities, version, author.
Does not depend on external YAML parsers.
"""

import re


def parse_frontmatter(content: str) -> dict | None:
    """
    Parse frontmatter from markdown content.
    
    Expected format:
    ---
    key: value
    ---
    body text
    """
    match = re.match(r'^---\s*\n([\s\S]*?)\s*\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return None
    
    fm_text = match.group(1)
    body = match.group(2)
    
    metadata = {}
    for line in fm_text.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        colon_pos = line.find(':')
        if colon_pos == -1:
            continue
        
        key = line[:colon_pos].strip()
        value = line[colon_pos + 1:].strip()
        
        # Remove quotes if present
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        
        # Parse array
        if value.startswith('[') and value.endswith(']'):
            inner = value[1:-1].strip()
            if inner:
                metadata[key] = [v.strip().strip('"').strip("'") for v in inner.split(',')]
            else:
                metadata[key] = []
        # Parse boolean
        elif value.lower() == 'true':
            metadata[key] = True
        elif value.lower() == 'false':
            metadata[key] = False
        # Parse integer
        elif re.match(r'^-?\d+$', value):
            metadata[key] = int(value)
        # Parse float
        elif re.match(r'^-?\d+\.\d+$', value):
            metadata[key] = float(value)
        else:
            metadata[key] = value
    
    return metadata


def is_valid_frontmatter(metadata: dict, required_fields: list) -> bool:
    """
    Check if metadata has all required fields.
    """
    for field in required_fields:
        if field not in metadata:
            return False
        val = metadata[field]
        if val is None:
            return False
        if isinstance(val, str) and val.strip() == '':
            return False
        if isinstance(val, list) and len(val) == 0:
            return False
    return True
