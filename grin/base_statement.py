from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .token import GrinToken

class Statement(ABC):
    @abstractmethod
    def execute(self, variables: Dict[str, Any], line_number: int) -> Optional[int]:
        """Execute the statement and return the next line number to execute"""
        pass

    def get_value(self, token: GrinToken, variables: Dict[str, Any]) -> Any:
        """Helper method to get value from token or variable"""
        from .token import GrinTokenKind
        if token.kind() in (GrinTokenKind.LITERAL_STRING, 
                           GrinTokenKind.LITERAL_INTEGER, 
                           GrinTokenKind.LITERAL_FLOAT):
            return token.value()
        return variables.get(token.text())
