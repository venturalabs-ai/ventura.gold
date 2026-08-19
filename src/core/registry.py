"""
Agent Registry - Discovers and registers agents and skills from JSON files.

Discovers JSON files inside src/agents and src/skills, parses metadata,
validates required fields, and maintains an internal index.
Preserves paths internally but does NOT include them in the exported manifest.
"""

import json
import os
from .frontmatter import parse_frontmatter, is_valid_frontmatter

AGENTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'agents')
SKILLS_DIR = os.path.join(os.path.dirname(__file__), '..', 'skills')


def discover_agents():
    """
    Discover all agent JSON files from the agents directory.
    """
    results = []
    
    if not os.path.exists(AGENTS_DIR):
        print(f"Warning: Agents directory not found: {AGENTS_DIR}")
        return results
    
    for filename in os.listdir(AGENTS_DIR):
        filepath = os.path.join(AGENTS_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        if not filename.endswith('.json'):
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            required = ['id', 'name', 'description', 'capabilities', 'version', 'author']
            if all(field in data and data[field] for field in required):
                results.append({
                    'file_path': f"src/agents/{filename}",
                    'id': data['id'],
                    'name': data['name'],
                    'description': data['description'],
                    'capabilities': data.get('capabilities', []),
                    'version': data.get('version', '0.1.0'),
                    'author': data.get('author', 'Unknown'),
                    'instructions': data.get('instructions', ''),
                })
            else:
                print(f"Warning: Invalid agent metadata in: {filepath}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    
    return results


def discover_skills():
    """
    Discover all skill JSON files from the skills directory.
    """
    results = []
    
    if not os.path.exists(SKILLS_DIR):
        print(f"Warning: Skills directory not found: {SKILLS_DIR}")
        return results
    
    for filename in os.listdir(SKILLS_DIR):
        filepath = os.path.join(SKILLS_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        if not filename.endswith('.json'):
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            required = ['id', 'name', 'description', 'capabilities', 'version', 'author']
            if all(field in data and data[field] for field in required):
                results.append({
                    'file_path': f"src/skills/{filename}",
                    'id': data['id'],
                    'name': data['name'],
                    'description': data['description'],
                    'capabilities': data.get('capabilities', []),
                    'version': data.get('version', '0.1.0'),
                    'author': data.get('author', 'Unknown'),
                    'instructions': data.get('instructions', ''),
                })
            else:
                print(f"Warning: Invalid skill metadata in: {filepath}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    
    return results


def validate_agent(agent: dict) -> dict:
    """
    Validate an agent entry has all required fields and no issues.
    """
    errors = []
    
    required = ['id', 'name', 'description', 'capabilities', 'version', 'author']
    for field in required:
        if field not in agent or not agent[field]:
            errors.append(f"Missing `{field}` field")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
    }


def validate_skill(skill: dict) -> dict:
    """
    Validate a skill entry has all required fields and no issues.
    """
    return validate_agent(skill)
