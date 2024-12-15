# src/scanner/__init__.py
"""
Vulnerability scanning module for repository security analysis.

This package provides tools for scanning repositories using semgrep 
and extracting potential security vulnerabilities.
"""

from .semgrep_scanner import SemgrepScanner

__all__ = ['SemgrepScanner']
