@echo off
echo ================================================================
echo Testing LegalMitra Enhanced Features
echo ================================================================
echo.

echo Test 1: Classify Query (Simple Question)
echo ----------------------------------------------------------------
curl -X POST "http://localhost:8888/api/v1/classify-query" -H "Content-Type: application/json" -d "{\"query\": \"What is Section 377 IPC?\"}"
echo.
echo.

echo Test 2: Enhanced Query Processing (Simple)
echo ----------------------------------------------------------------
curl -X POST "http://localhost:8888/api/v1/enhanced-query" -H "Content-Type: application/json" -d "{\"query\": \"Explain what is bail?\", \"query_type\": \"research\"}"
echo.
echo.

echo Test 3: Model Health Check
echo ----------------------------------------------------------------
curl "http://localhost:8888/api/v1/model-health"
echo.
echo.

echo Test 4: Cost Savings Report
echo ----------------------------------------------------------------
curl "http://localhost:8888/api/v1/cost-savings-report"
echo.
echo.

echo ================================================================
echo Testing Complete!
echo ================================================================
pause
