from ai_orchestrator.prompts.test_prompt import TEST_GENERATION_PROMPT
from ai_orchestrator.llm_client import call_llm


class TestGeneratorAgent:

    def generate(self, bdd):
        prompt = TEST_GENERATION_PROMPT.format(bdd=bdd)
        return call_llm(prompt)
    
    
    