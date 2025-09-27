
import os
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from typing import Any, Optional

class Configuration(BaseModel):
    """The configuration for the agent."""

    planning_agent_model: str = Field(
        default="gpt-oss:20b",
        metadata={
            "description": "Language model used for agent planning."
        },
    )
    relevance_agent_model: str = Field(
        default="llama3.1:8b",
        metadata={
            "description": "Language model used for agent relevance assessment."
        },
    )
    executor_model: str = Field(
        default="llama3.1:8b",
        metadata={
            "description": "Language model used for agent tool execution."
        },
    )

    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        
        configurable = (config["configurable"] if config and "configurable" in config else {})

        raw_values: dict[str, Any] = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }

        values = {k: v for k, v in raw_values.items() if v is not None}
        return cls(**values)