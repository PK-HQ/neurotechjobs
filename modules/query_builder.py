# modules/query_builder.py

from config.settings import KEYWORDS

def generate_dynamic_query():
    """Generate a dynamic query based on manually entered keywords."""
    return " OR ".join(KEYWORDS)
