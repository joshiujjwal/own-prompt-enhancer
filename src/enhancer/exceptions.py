"""Custom exceptions for OwnPromptEnhancer."""


class OPEError(Exception):
    """Base exception for all OPE errors."""


class PromptTooLongError(OPEError):
    """Raised when the prompt exceeds MAX_PROMPT_LENGTH characters."""

    def __init__(self, length: int, max_length: int) -> None:
        super().__init__(
            f"Prompt length {length} exceeds maximum allowed {max_length} characters."
        )
        self.length = length
        self.max_length = max_length


class UnknownStrategyError(OPEError):
    """Raised when an unrecognised strategy ID is requested."""

    def __init__(self, strategy_id: str) -> None:
        super().__init__(f"Unknown strategy: '{strategy_id}'")
        self.strategy_id = strategy_id


class AdapterError(OPEError):
    """Raised when an upstream LLM adapter call fails."""

    def __init__(self, adapter: str, detail: str) -> None:
        super().__init__(f"Adapter '{adapter}' failed: {detail}")
        self.adapter = adapter
        self.detail = detail
