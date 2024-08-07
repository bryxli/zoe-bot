Feature: League command scenarios

    Scenario Outline: adduser with valid guild
        Given guild has been initialized
        When adduser <gameName>:<tag>
        Then bot sends <output>

        Examples:
            | gameName | tag | output                        |
            | bryxli   | NA1 | player registered             |
            | GN       | NA1 | please enter a valid username |

    Scenario Outline: adduser with valid guild and user exists
        Given guild has been initialized
        When adduser bryxli:NA1
        And adduser <gameName>:<tag>
        Then bot sends <output>

        Examples:
            | gameName | tag | output                        |
            | bryxli   | NA1 | player already exists         |

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
            | GN       | NA1 | please enter a valid username |
    
    Scenario Outline: deluser with valid guild and user does not exist
        Given guild has been initialized
        When deluser <gameName>:<tag>
        Then bot sends <output>

        Examples:
            | gameName | tag | output                        |
            | bryxli   | NA1 | player not registered         |

    Scenario Outline: deluser with invalid guild
        Given guild has not been initialized
        When deluser <gameName>:<tag>
        Then bot sends <output>

        Examples:
            | gameName | tag | output               |
            | bryxli   | NA1 | guild not registered |

    Scenario Outline: userlist with valid guild and populated userlist
        Given guild has been initialized
        And a set of added players
            | gameName | tag |
            | bryxli   | NA1 |
        When userlist
        Then bot sends <output>

        Examples:
            | output |
            | bryxli |

    Scenario Outline: userlist with valid guild and unpopulated userlist
        Given guild has been initialized
        When userlist
        Then bot sends <output>

        Examples:
            | output                  |
            | no users are registered |

    Scenario Outline: userlist with invalid guild
        Given guild has not been initialized
        When userlist
        Then bot sends <output>

        Examples:
            | output               |
            | guild not registered |
