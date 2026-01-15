from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import os
from pathlib import Path
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class BaseAgent(ABC):
    def __init__(self, name: str, model: str = "gpt-4o-mini", temperature: float = 0.7):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.client = OpenAI()
        self.async_client = AsyncOpenAI()
        self.conversation_history = []
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    def call_llm(
        self,
        user_message: str,
        response_format: Optional[type[BaseModel]] = None,
        max_tokens: int = 4000
    ) -> str | BaseModel:
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            *self.conversation_history,
            {"role": "user", "content": user_message}
        ]
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": max_tokens,
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = self.client.beta.chat.completions.parse(**kwargs)
        
        if response_format:
            return response.choices[0].message.parsed
        
        content = response.choices[0].message.content
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": content})
        
        return content
    
    def call_llm_json(self, user_message: str, max_tokens: int = 4000) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def call_llm_json_async(self, user_message: str, max_tokens: int = 4000) -> Dict[str, Any]:
        """Async version of call_llm_json for true concurrent operations."""
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": user_message}
        ]
        
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def reset_conversation(self):
        self.conversation_history = []
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass