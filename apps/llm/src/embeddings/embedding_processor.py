# src/embeddings/embedding_processor.py
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from typing import List, Dict
import torch

class VulnerabilityMatcher:
    def __init__(self, cwe_path: str, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name, device='cpu')  # Force CPU usage
        self.cwe_df = pd.read_csv(cwe_path)
        self._prepare_cwe_embeddings()
        
    def _prepare_cwe_embeddings(self):
        """
        Prepare embeddings for CWE descriptions
        """
        # Combine relevant columns for better matching
        self.cwe_df['combined_text'] = self.cwe_df.apply(
            lambda row: f"{row['Name']} {row['Description']}", axis=1
        )
        
        # Generate embeddings for all CWE entries
        self.cwe_embeddings = self.model.encode(
            self.cwe_df['combined_text'].tolist(),
            convert_to_tensor=False  # Get numpy array instead of tensor
        )
        print('DONE')
        print(self.cwe_embeddings.shape)
        
    def match_vulnerability(self, finding: Dict) -> Dict:
        """
        Match a single vulnerability finding with CWE database
        """
        # Create a combined text from the finding
        finding_text = f"{finding['message']} {finding.get('code', '')}"
        
        # Generate embedding for the finding
        finding_embedding = self.model.encode(
            finding_text,
            convert_to_tensor=False  # Get numpy array instead of tensor
        )
        
        # Calculate cosine similarity using numpy
        # Normalize vectors
        finding_norm = np.linalg.norm(finding_embedding)
        cwe_norms = np.linalg.norm(self.cwe_embeddings, axis=1)
        
        # Calculate dot product and divide by norms
        cos_scores = np.dot(self.cwe_embeddings, finding_embedding) / (cwe_norms * finding_norm)
        
        # Get top matches
        top_k = 3
        top_indices = np.argsort(cos_scores)[-top_k:][::-1]
        top_scores = cos_scores[top_indices]
        
        matches = []
        for idx, score in zip(top_indices, top_scores):
            matches.append({
                'cwe_id': self.cwe_df.iloc[int(idx)]['CWE-ID'],
                'name': self.cwe_df.iloc[int(idx)]['Name'],
                'description': self.cwe_df.iloc[int(idx)]['Description'],
                'confidence': float(score)
            })

        print(matches)
            
        finding['cwe_matches'] = matches
        return finding
