class BDDAgent:

    def generate(self, story):

        return f"""
Feature: {story['title']}

Scenario: Basic flow
Given user is on login page
When user enters valid credentials
Then user should see dashboard
"""
    