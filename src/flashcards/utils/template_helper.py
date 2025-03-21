from datetime import datetime
from typing import Dict, Any

def get_common_context() -> Dict[str, Any]:
    """
    Generate common context data for templates
    """
    return {
        "now": {"year": datetime.now().year},
        "nav_info": {"current_path": ""}  # Will be updated in routes
    } 