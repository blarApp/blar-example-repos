def current_date() -> str:
    """Return the current date as a string."""
    return datetime.now().strftime("%Y-%m-%d")

def current_time() -> str:
    """Return the current time as a string."""
    return datetime.now().strftime("%H:%M:%S")

def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a given datetime object as a string."""
    return dt.strftime(fmt)
