# usage_example.py
from src.main import SecurityScanOrchestrator

# Initialize the orchestrator
orchestrator = SecurityScanOrchestrator(
    repo_path="/home/kglinsk/Desktop/test_fold",
    cwe_path="./CWE.csv",
    openai_api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVjNjg5NTQ4LWMxYWItNGYzOC05NDc0LTYzMDg2Njk2OTU1MSIsImlzRGV2ZWxvcGVyIjp0cnVlLCJpYXQiOjE2ODYwNTI5MTIsImV4cCI6MjAwMTYyODkxMn0.-9hxyZk_aqtLuF345ErIlNU8mOgXdAgy13OBKiOPSO8"
)

# Run the analysis
report = orchestrator.run_analysis()
print(report)
