# src/scanner/semgrep_scanner.py
import subprocess
import json
from typing import List, Dict
from pathlib import Path

class SemgrepScanner:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        
    def run_scan(self) -> List[Dict]:
        """
        Runs semgrep scan and returns the results as a list of findings
        """
        try:
            # Run semgrep with JSON output
            cmd = [
                "semgrep",
                "--config=auto",  # Use default rules
                "--json",
                str(self.repo_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            print(result)
            
            if result.returncode != 0:
                raise Exception(f"Semgrep scan failed: {result.stderr}")
                
            findings = json.loads(result.stdout)
            return self._parse_findings(findings)
            
        except Exception as e:
            raise Exception(f"Error during semgrep scan: {str(e)}")
    
    def _parse_findings(self, raw_findings: Dict) -> List[Dict]:
        """
        Parse semgrep output into a structured format
        """
        parsed_findings = []
        
        for result in raw_findings.get('results', []):
            finding = {
                'file': result.get('path'),
                'line': result.get('start', {}).get('line'),
                'message': result.get('extra', {}).get('message'),
                'severity': result.get('extra', {}).get('severity'),
                'rule_id': result.get('check_id'),
                'code': result.get('extra', {}).get('lines')
            }
            parsed_findings.append(finding)
            
        return parsed_findings
