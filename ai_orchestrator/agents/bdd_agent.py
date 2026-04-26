from ai_orchestrator.prompts.bdd_prompt import BDD_PROMPT
from ai_orchestrator.llm_client import call_llm


class BDDAgent:

    def generate(self, story):
        prompt = BDD_PROMPT.format(story=story)
        return call_llm(prompt)
    
    