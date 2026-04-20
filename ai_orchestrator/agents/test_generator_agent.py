class TestGeneratorAgent:

    def generate(self, bdd):

        return f"""
def test_generated_flow():
    # Generated from BDD
    assert True
"""
    