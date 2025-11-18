"""Database models."""
# Lazy imports to avoid circular dependency issues
__all__ = ["Analysis", "Clause"]

def __getattr__(name):
    if name == "Analysis":
        from app.models.analysis import Analysis
        return Analysis
    elif name == "Clause":
        from app.models.analysis import Clause
        return Clause
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

