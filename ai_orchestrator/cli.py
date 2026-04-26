import click
import webbrowser
import pathlib
from ai_orchestrator.orchestrator import QAOrchestrator


@click.command()
@click.option("--story", default=None, help="Jira story ID to run pipeline")
@click.option("--pr", default=None, help="PR ID to review")
@click.option("--branch", default=None, help="Branch name to review e.g. main")
def run(story, pr, branch):
    orchestrator = QAOrchestrator()

    if story:
        result = orchestrator.run_pipeline(story_id=story)

        print("\n========== STORY ==========")
        print(result["story"])

        print("\n========== GENERATED BDD ==========")
        print(result["bdd"])

        print("\n========== GENERATED TEST CODE ==========")
        print(result["test_code"])

        print("\n========== SAVED FILES ==========")
        print(f"BDD feature : {result['bdd_saved_to']}")
        print(f"Test file   : {result['test_saved_to']}")

        print("\n========== EXECUTION ==========")
        print(f"Status   : {result['execution']['status']}")
        print(f"Exit code: {result['execution']['returncode']}")
        print(result["execution"]["stdout"])

    elif pr:
        result = orchestrator.review_pipeline(pr_id=pr)

        print("\n========== PR REVIEW ==========")
        print(result["review"])

        print("\n========== SAVED FILES ==========")
        print(f"Markdown    : {result['review_saved_to']}")
        print(f"HTML report : {result['report_saved_to']}")

        webbrowser.open(pathlib.Path(result["report_saved_to"]).resolve().as_uri())

    elif branch:
        result = orchestrator.branch_review_pipeline(branch=branch)

        print("\n========== BRANCH REVIEW ==========")
        print(result["review"])

        print("\n========== SAVED FILES ==========")
        print(f"Markdown    : {result['review_saved_to']}")
        print(f"HTML report : {result['report_saved_to']}")

        webbrowser.open(pathlib.Path(result["report_saved_to"]).resolve().as_uri())

    else:
        print("Provide --story <id>, --pr <id>, or --branch <name>")


if __name__ == "__main__":
    run()
    

    

    