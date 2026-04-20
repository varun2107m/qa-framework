import click
from ai_orchestrator.orchestrator import QAOrchestrator


@click.command()
@click.option("--story", required=True)
@click.option("--pr", required=False)

def run(story, pr):
    orchestrator = QAOrchestrator()
    result = orchestrator.run_pipeline(story_id=story, pr_id=pr)

    print("\n===== FINAL OUTPUT =====")
    print(result)


if __name__ == "__main__":
    run()
    