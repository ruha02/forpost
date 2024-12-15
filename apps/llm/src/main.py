from typing import List, Dict
import os
from src.scanner.semgrep_scanner import SemgrepScanner
from src.embeddings.embedding_processor import VulnerabilityMatcher
from openai import OpenAI
from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')

class SecurityScanOrchestrator:
    def __init__(self, repo_path: str, cwe_path: str, openai_api_key: str, base_url: str = OPENAI_BASE_URL):
        self.repo_path = repo_path
        self.scanner = SemgrepScanner(repo_path)
        self.matcher = VulnerabilityMatcher(cwe_path)
        self.client = OpenAI(
            api_key=openai_api_key,
            base_url=base_url
        )
        
    def run_analysis(self) -> str:
        """
        Run the complete security analysis pipeline
        """
        # 1. Run semgrep scan
        findings = self.scanner.run_scan()
        
        # 2. Match vulnerabilities with CWE
        enriched_findings = []
        for finding in findings:
            enriched_finding = self.matcher.match_vulnerability(finding)
            print(enriched_finding)
            enriched_findings.append(enriched_finding)
            
        # 3. Generate report using GPT
        report = self._generate_report(enriched_findings)
        
        return report
    
    def _generate_report(self, findings: List[Dict]) -> str:
        """
        Generate a concise report using GPT
        """
        # Prepare the findings summary for GPT
        findings_summary = self._prepare_findings_summary(findings)
        
        prompt = f"""
Проанализируйте следующие результаты сканирования безопасности и создайте развернутый, системный и 
структурированный отчет. Сосредоточьтесь на:
1. Критических и высокосерьезных проблемах
2. Наиболее вероятных уязвимостях по классификации CWE
3. Рекомендуемых действиях
        Findings:
        {findings_summary}
        """
        
        response = self.client.chat.completions.create(
            model="qwen-2.5-72b-instruct",
            messages=[
                {"role": "system", "content": "Ты - эксперт в области кибербезопасности и защищенного ПО. Отвечай на русском языке"},
                {"role": "user", "content": prompt}
            ]
        )
        print(response)
        
        return response.choices[0].message.content
    
    def _prepare_findings_summary(self, findings: List[Dict]) -> str:
        """
        Convert findings into a structured summary for GPT
        """
        summary = []
        for finding in findings:
            summary.append(
                f"File: {finding['file']}\n"
                f"Line: {finding['line']}\n"
                f"Severity: {finding['severity']}\n"
                f"Message: {finding['message']}\n"
                f"Top CWE Match: {finding['cwe_matches'][0]['cwe_id']} - "
                f"{finding['cwe_matches'][0]['name']}\n"
                f"Code: {finding.get('code', 'N/A')}\n"
                "---"
            )

        print("\n".join(summary))
        return "\n".join(summary)
