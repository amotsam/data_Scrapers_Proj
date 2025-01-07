from datetime import datetime

def current_timestamp():
    """Returns the current timestamp as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
