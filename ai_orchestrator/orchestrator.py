from ai_orchestrator.mcp.jira_mcp import JiraMCP
from ai_orchestrator.mcp.github_mcp import GitHubMCP
from ai_orchestrator.mcp.playwright_mcp import PlaywrightMCP

from ai_orchestrator.agents.bdd_agent import BDDAgent
from ai_orchestrator.agents.test_generator_agent import TestGeneratorAgent


class QAOrchestrator:

    def __init__(self):
        self.jira = JiraMCP()
        self.github = GitHubMCP()
        self.playwright = PlaywrightMCP()

        self.bdd = BDDAgent()
        self.testgen = TestGeneratorAgent()

    def run_pipeline(self, story_id, pr_id=None):

        # 1. Jira Story
        story = self.jira.get_story(story_id)

        # 2. BDD generation
        bdd = self.bdd.generate(story)

        # 3. Test generation
        tests = self.testgen.generate(bdd)

        # 4. GitHub analysis (optional)
        pr_analysis = None
        if pr_id:
            pr_analysis = self.github.analyze_pr(pr_id)

        # 5. Execute existing Playwright framework safely
        execution = self.playwright.run_smoke_flow()

        return {
            "story": story,
            "bdd": bdd,
            "tests": tests,
            "pr_analysis": pr_analysis,
            "execution": execution
        }
    