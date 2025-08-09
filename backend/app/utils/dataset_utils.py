import pandas as pd
import json
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class DatasetUtils:
    def __init__(self):
        self.datasets = {}
    
    async def load_dataset(self, file_path: str) -> pd.DataFrame:
        """Load a dataset from file"""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                return pd.read_json(file_path)
            elif file_path.endswith('.xlsx'):
                return pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
                
        except Exception as e:
            logger.error(f"Error loading dataset {file_path}: {e}")
            raise
    
    async def search_dataset(self, dataset: pd.DataFrame, query: str) -> List[Dict[str, Any]]:
        """Search within a dataset"""
        try:
            # Simple text search implementation
            results = []
            for column in dataset.columns:
                if dataset[column].dtype == 'object':
                    matches = dataset[dataset[column].str.contains(query, case=False, na=False)]
                    if not matches.empty:
                        results.extend(matches.to_dict('records'))
            
            return results[:10]  # Limit to 10 results
            
        except Exception as e:
            logger.error(f"Error searching dataset: {e}")
            return []
    
    async def get_dataset_info(self, dataset: pd.DataFrame) -> Dict[str, Any]:
        """Get information about a dataset"""
        return {
            "shape": dataset.shape,
            "columns": list(dataset.columns),
            "dtypes": dataset.dtypes.to_dict(),
            "missing_values": dataset.isnull().sum().to_dict(),
            "summary": dataset.describe().to_dict()
        } 