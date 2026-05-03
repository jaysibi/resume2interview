"""Direct call to endpoint function to see actual error"""
import sys
import traceback
from dotenv import load_dotenv
load_dotenv()

# Import after dotenv
from db import SessionLocal
from main import gap_analysis
from fastapi import Request
from unittest.mock import Mock

# Create mock request
mock_request = Mock(spec=Request)
mock_request.client = Mock()
mock_request.client.host = "127.0.0.1"

# Create DB session
db = SessionLocal()

try:
    print("Calling gap_analysis directly...")
    import asyncio
    result = asyncio.run(gap_analysis(mock_request, 5, 4, db))
    print(f"Result: {result}")
except Exception as e:
    print(f"\n!!! EXCEPTION: {type(e).__name__}: {str(e)}")
    print("\n!!! FULL TRACEBACK:")
    traceback.print_exc()
finally:
    db.close()
