Feature: League command scenarios

    Scenario Outline: adduser with valid guild
        Given guild has been initialized
        When adduser <gameName>:<tag>
        Then bot sends <output>

        Examples:
            | gameName | tag | output                        |
            | bryxli   | NA1 | player registered             |
            # TODO: create test case for existing user (userlist is cleared on every case)
            # | bryxli   | NA1 | player already exists         |
            | GN       | NA1 | please enter a valid username |

    Scenario Outline: adduser with invalid guild
        Given guild has not been initialized
        When adduser <gameName>:<tag>
        Then bot sends <output>

        Examples:
            | gameName | tag | output               |
            | bryxli   | NA1 | guild not registered |

    Scenario Outline: deluser with valid guild
        Given guild has been initialized
        When adduser <gameName>:<tag>
        And deluser <gameName>:<tag>
        Then bot sends <output>

        Examples:
            | gameName | tag | output                        |
            | bryxli   | NA1 | player deleted                |
            # TODO: create test case for no existing user (adduser is run on every case)
            # | bryxli   | NA1 | player not registered         |
            | GN       | NA1 | please enter a valid username |

    Scenario Outline: deluser with invalid guild
        Given guild has not been initialized
        When deluser <gameName>:<tag>
        Then bot sends <output>

        Examples:
            | gameName | tag | output               |
            | bryxli   | NA1 | guild not registered |

    # TODO: uncomment userlist scenarios post-implementation

    # Scenario Outline: userlist with valid guild and populated userlist
    #     Given guild has been initialized
    #     And a set of added players
    #         | gameName | tag |
    #         | bryxli   | NA1 |
    #     When userlist
    #     Then bot sends <output>

    #     Examples:
    #         | output |
    #         | bryxli |

    # Scenario Outline: userlist with valid guild and unpopulated userlist
    #     Given guild has been initialized
    #     When userlist
    #     Then bot sends <output>

    #     Examples:
    #         | output                  |
    #         | no users are registered |

    # Scenario Outline: userlist with invalid guild
    #     Given guild has not been initialized
    #     When userlist
    #     Then bot sends <output>

    #     Examples:
    #         | output               |
    #         | guild not registered |
