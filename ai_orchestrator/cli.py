import click
from ai_orchestrator.orchestrator import QAOrchestrator


@click.command()
@click.option("--story", required=True)

def run(story):
    orchestrator = QAOrchestrator()
    result = orchestrator.run_pipeline(story_id=story)

    print("\n===== OUTPUT =====")
    print(result)


if __name__ == "__main__":
    run()
    