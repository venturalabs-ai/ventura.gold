# Architecture

Local-first agent framework with optional LLM calls.

Flow: prompt → registry → router → runtime (instructions) → optional LLMClient → output.

MCP-style servers provide git/fs tools used by repository skills.
