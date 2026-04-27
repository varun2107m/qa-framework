import os

from ai_orchestrator.mcp.playwright_mcp import PlaywrightMCP
from ai_orchestrator.mcp.jira_mcp import JiraMCP
from ai_orchestrator.mcp.github_mcp import GitHubMCP
from ai_orchestrator.agents.bdd_agent import BDDAgent
from ai_orchestrator.agents.test_generator_agent import TestGeneratorAgent
from ai_orchestrator.prompts.review_prompt import CODE_REVIEW_PROMPT
from ai_orchestrator.llm_client import call_llm
from ai_orchestrator.report_generator import generate_pr_report


class QAOrchestrator:

    def __init__(self):
        self.playwright = PlaywrightMCP()
        self.jira = JiraMCP()
        self.github = GitHubMCP()
        self.bdd = BDDAgent()
        self.testgen = TestGeneratorAgent()

        self.features_dir = "ai_orchestrator/generated/features"
        self.tests_dir = "ai_orchestrator/generated/tests"
        self.reviews_dir = "ai_orchestrator/generated/reviews"

        # ✅ create all output dirs on init — same pattern already used in conftest.py
        for d in (self.features_dir, self.tests_dir, self.reviews_dir):
            os.makedirs(d, exist_ok=True)

    def run_pipeline(self, story_id):

        # 1. Fetch story from Jira
        story = self.jira.get_story(story_id)

        # 2. Generate BDD and save to features folder
        bdd = self.bdd.generate(story)
        feature_file = os.path.join(self.features_dir, f"{story_id}.feature")
        with open(feature_file, "w") as f:
            f.write(bdd)

        # 3. Generate test and save to tests folder
        test_code = self.testgen.generate(bdd)
        test_file = os.path.join(self.tests_dir, f"test_{story_id}.py")
        with open(test_file, "w") as f:
            f.write(test_code)

        # 4. Execute existing framework flow
        execution = self.playwright.run_smoke_flow()

        return {
            "story": story,
            "bdd": bdd,
            "bdd_saved_to": feature_file,
            "test_code": test_code,
            "test_saved_to": test_file,
            "execution": execution
        }

    def review_pipeline(self, pr_id):

        # 1. Fetch PR data from GitHub
        pr_data = self.github.analyze_pr(pr_id)

        # 2. Build review prompt and call LLM
        prompt = CODE_REVIEW_PROMPT.format(diff=pr_data)
        review = call_llm(prompt)

        # 3. Save markdown
        review_file = os.path.join(self.reviews_dir, f"pr_{pr_id}_review.md")
        with open(review_file, "w") as f:
            f.write(f"# PR {pr_id} Review\n\n")
            f.write(f"**Title:** {pr_data.get('title', 'N/A')}\n\n")
            f.write(f"**Changed Files:**\n")
            for file in pr_data.get("changed_files", []):
                f.write(f"- {file}\n")
            f.write(f"\n## AI Review\n\n")
            f.write(review)

        # 4. Save HTML report
        report_html = generate_pr_report(pr_data, review, pr_id)
        report_file = os.path.join(self.reviews_dir, f"pr_{pr_id}_report.html")
        with open(report_file, "w") as f:
            f.write(report_html)

        return {
            "pr_id": pr_id,
            "pr_data": pr_data,
            "review": review,
            "review_saved_to": review_file,
            "report_saved_to": report_file
        }

    def branch_review_pipeline(self, branch="main"):

        # 1. Fetch branch data from GitHub
        pr_data = self.github.analyze_branch(branch)

        # 2. Build review prompt and call LLM
        prompt = CODE_REVIEW_PROMPT.format(diff=pr_data)
        review = call_llm(prompt)

        # 3. Save markdown
        review_file = os.path.join(self.reviews_dir, f"branch_{branch}_review.md")
        with open(review_file, "w") as f:
            f.write(f"# Branch Review: {branch}\n\n")
            f.write(f"**Repo:** {os.getenv('GITHUB_REPO')}\n\n")
            f.write(f"**Files:**\n")
            for file in pr_data.get("changed_files", []):
                f.write(f"- {file}\n")
            f.write(f"\n## AI Review\n\n")
            f.write(review)

        # 4. Save HTML report
        report_html = generate_pr_report(pr_data, review, branch)
        report_file = os.path.join(self.reviews_dir, f"branch_{branch}_report.html")
        with open(report_file, "w") as f:
            f.write(report_html)

        return {
            "branch": branch,
            "pr_data": pr_data,
            "review": review,
            "review_saved_to": review_file,
            "report_saved_to": report_file
        }
    

    