"""
LLM Service for interfacing with Groq and OpenAI APIs
"""
import os
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Default model candidates for Groq in order of preference
GROQ_DEFAULT_MODEL = "openai/gpt-oss-120b"
GROQ_FALLBACK_MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b",
    "groq/compound",
]


class LLMService:
    """Service for calling the LLM API with resilient fallback support"""

    @classmethod
    def get_provider(cls) -> str:
        """Get the configured LLM provider"""
        return os.getenv("LLM_PROVIDER", "groq").lower().strip()

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get the configured LLM API key"""
        return os.getenv("LLM_API_KEY")

    @classmethod
    def get_configured_model(cls) -> str:
        """Get configured model or provider default"""
        provider = cls.get_provider()
        if provider == "groq":
            model = os.getenv("LLM_MODEL", GROQ_DEFAULT_MODEL).strip()
            # If an old deprecated model was left in env, update to default
            if model in ["llama-3.1-8b-instant", "llama3-8b-8192", "llama3-70b-8192"]:
                return GROQ_DEFAULT_MODEL
            return model or GROQ_DEFAULT_MODEL
        else:
            return os.getenv("LLM_MODEL", "gpt-4o-mini").strip()

    @classmethod
    def call_llm(
        cls,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Call the LLM and get a response.

        Args:
            system_prompt: System instructions for the LLM
            user_message: Current user message
            temperature: Temperature for response variability
            max_tokens: Maximum tokens in response
            conversation_history: Previous conversation messages

        Returns:
            LLM response text
        """
        provider = cls.get_provider()
        api_key = cls.get_api_key()

        if not api_key:
            raise Exception("LLM API key is not configured. Check LLM_API_KEY in your .env file.")

        # Build messages list
        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})

        if provider == "groq":
            return cls._call_groq(
                api_key=api_key,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
        elif provider == "openai":
            return cls._call_openai(
                api_key=api_key,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            raise Exception(f"Unsupported LLM provider: '{provider}'. Supported providers are 'groq' and 'openai'.")

    @classmethod
    def _call_groq(
        cls,
        api_key: str,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call Groq API with automatic model fallback if a model is unavailable"""
        try:
            from groq import Groq
        except ImportError:
            raise Exception("The 'groq' Python package is not installed. Please run: pip install groq")

        client = Groq(api_key=api_key)
        preferred_model = cls.get_configured_model()

        # Build list of models to try starting with preferred model
        models_to_try = [preferred_model]
        for fallback in GROQ_FALLBACK_MODELS:
            if fallback not in models_to_try:
                models_to_try.append(fallback)

        last_error = None
        for model_name in models_to_try:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                content = response.choices[0].message.content
                if content:
                    return content.strip()
            except Exception as e:
                err_str = str(e)
                last_error = e
                # Check for model not found or deprecated
                if "model_not_found" in err_str or "404" in err_str or "does not exist" in err_str:
                    logger.warning("Groq model '%s' not found. Trying fallback model...", model_name)
                    continue
                elif "401" in err_str or "authentication" in err_str.lower():
                    raise Exception("Groq authentication failed. Please check that your Groq API key is valid.")
                else:
                    raise Exception(f"Error calling Groq LLM: {err_str}")

        raise Exception(f"Error calling Groq LLM: {str(last_error)}")

    @classmethod
    def _call_openai(
        cls,
        api_key: str,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call OpenAI API"""
        try:
            from openai import OpenAI, AuthenticationError, APIError
        except ImportError:
            raise Exception("The 'openai' Python package is not installed. Please run: pip install openai")

        client = OpenAI(api_key=api_key)
        model = cls.get_configured_model()

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            content = response.choices[0].message.content
            if not content:
                raise Exception("OpenAI returned an empty response.")
            return content.strip()
        except AuthenticationError as e:
            raise Exception(f"OpenAI authentication failed: {str(e)}")
        except APIError as e:
            raise Exception(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calling OpenAI LLM: {str(e)}")

    @classmethod
    def validate_api_key(cls) -> bool:
        """Validate that the LLM API key is configured properly"""
        api_key = cls.get_api_key()
        provider = cls.get_provider()

        if not api_key:
            return False

        if "your_" in api_key.lower() or "your_new" in api_key.lower():
            return False

        if provider == "groq" and not api_key.startswith("gsk_"):
            return False

        return True