"""
Configuration for the agent
"""
import os
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from typing import Any, Optional

class Configuration(BaseModel):
    """The configuration for the agent."""
    gatekeeper_agent_model: str = Field(
        default="qwen2.5-1.5b-instruct-q4_k_m.gguf",
        metadata={
            "description": "Language model used for agent gatekeeper assessment."
        },
    )
    planning_agent_model: str = Field(
        default="qwen2.5-1.5b-instruct-q4_k_m.gguf",
        metadata={
            "description": "Language model used for agent planning."
        },
    )
    executor_model: str = Field(
        default="qwen2.5-1.5b-instruct-q4_k_m.gguf",
        metadata={
            "description": "Language model used for agent tool execution."
        },
    )
    wish_generator_model: str = Field(
        default="qwen2.5-1.5b-instruct-q4_k_m.gguf",
        metadata={
            "description": "Language model used for wish generation."
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