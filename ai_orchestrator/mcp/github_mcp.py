class GitHubMCP:

    def analyze_pr(self, pr_id):
        return {
            "pr_id": pr_id,
            "risk": "medium",
            "summary": "Login module changed"
        }
    