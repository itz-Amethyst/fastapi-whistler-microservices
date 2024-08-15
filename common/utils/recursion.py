# Credit https://github.com/aybruhm/fastapi-odmantic/blob/main/backend/apps/commoners/utils.py
import sys

class RecursionDepth:
    """
    A Context manager that temporarily set the recursion depth limit.
    """
    
    def __init__(self, limit: int):
        self.limit = limit
        self.default_limit = sys.getrecursionlimit()
        
    def __enter__(self):
        sys.setrecursionlimit(self.limit)
        
    def __exit__(self, exc_type, exc_value, traceback):
        sys.setrecursionlimit(self.default_limit)