from ai_orchestrator.mcp.playwright_mcp import PlaywrightMCP
from ai_orchestrator.agents.bdd_agent import BDDAgent
from ai_orchestrator.agents.test_generator_agent import TestGeneratorAgent


class QAOrchestrator:

    def __init__(self):
        self.playwright = PlaywrightMCP()
        self.bdd = BDDAgent()
        self.testgen = TestGeneratorAgent()

    def run_pipeline(self, story_id):

        # 1. MOCK Jira story (keep simple for now)
        story = {
            "id": story_id,
            "title": "Login feature",
            "description": "User should login with valid credentials"
        }

        # 2. Generate BDD
        bdd = self.bdd.generate(story)

        # 3. Generate test
        test_code = self.testgen.generate(bdd)

        # 4. Execute REAL existing framework flow
        execution = self.playwright.run_smoke_flow()

        return {
            "story": story,
            "bdd": bdd,
            "test_code": test_code,
            "execution": execution
        }
    