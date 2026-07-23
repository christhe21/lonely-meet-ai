"""
Brain – LLM + persona system prompt.

Receives finalized transcript segments and produces persona-aligned responses.
"""

class LLMPersona:
    def __init__(self, system_prompt: str, model: str = "gpt-4o"):
        self.system_prompt = system_prompt
        self.model = model

    async def generate_response(self, transcript: str, history: list | None = None) -> str:
        raise NotImplementedError("LLM call + persona prompting not yet implemented")
