# src/utils/errors.py

class AIHubError(Exception):
    """Base exception for AI Hub."""
    pass


class APIKeyMissingError(AIHubError):
    """Raised when API key is not found or configured."""
    def __init__(self, service: str):
        super().__init__(f"API key for '{service}' is missing. Please configure it in settings.")


class APIRequestError(AIHubError):
    """Raised when a request to an AI API fails."""
    def __init__(self, service: str, status: int, message: str):
        super().__init__(f"{service} API request failed with status {status}: {message}")


class ConfigLoadError(AIHubError):
    """Raised when config loading or parsing fails."""
    def __init__(self, message: str):
        super().__init__(f"Configuration load error: {message}")
