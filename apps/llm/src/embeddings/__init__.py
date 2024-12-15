# src/embeddings/__init__.py
"""
Embedding and vulnerability matching module.

Provides functionality for matching vulnerabilities using semantic embeddings
and comparing against a CWE database.
"""

from .embedding_processor import VulnerabilityMatcher

__all__ = ['VulnerabilityMatcher']


