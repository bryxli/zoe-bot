Feature: Main command scenarios

    Scenario: help
        Given help
        Then bot sends command information

    Scenario: speak
        Given speak
        Then bot sends a random voice line
