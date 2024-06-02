Feature: Server command scenarios

    Scenario Outline: setup success
        Given guild has not been initialized
        When setup
        Then bot sends <output>

        Examples:
            | output            |
            | guild initialized |

    Scenario Outline: setup failure
        Given guild has been initialized
        When setup
        Then bot sends <output>

        Examples:
            | output               |
            | guild already exists |

    Scenario Outline: reset success
        Given guild has been initialized
        And guild has been acknowledged
        When reset
        Then bot sends <output>

        Examples:
            | output        |
            | guild deleted |

    Scenario Outline: reset unacknowledged
        Given guild has been initialized
        When reset
        Then bot sends <output>

        Examples:
            | output                                                                                                                         |
            | this action can be harmful, running /reset or /region <region> will delete all registered users. acknowledge with /acknowledge |

    Scenario Outline: reset failure
        Given guild has not been initialized
        When reset
        Then bot sends <output>

        Examples:
            | output               |
            | guild not registered |

    Scenario Outline: region success
        Given guild has been initialized
        And guild has been acknowledged
        When region <region>
        Then bot sends <output>

        Examples:
            | region | output                                                |
            | KR     | guild region changed                                  |
            | foo    | region not found                                      |
            # TODO: create test case for empty region (not throwing KeyError Exception)
            # | ""     | BR EUNE EUW JP KR LAN LAS NA OCE TR RU PH SG TH TW VN |


    Scenario Outline: region unacknowledged
        Given guild has been initialized
        When region <region>
        Then bot sends <output>

        Examples:
            | region | output                                                                                                                         |
            | KR     | this action can be harmful, running /reset or /region <region> will delete all registered users. acknowledge with /acknowledge |

    Scenario Outline: region failure
        Given guild has not been initialized
        When region <region>
        Then bot sends <output>

        Examples:
            | region | output               |
            | KR     | guild not registered |

    Scenario Outline: acknowledge with valid guild
        Given guild has been initialized
        When acknowledge
        Then bot sends <output>

        Examples:
            | output                    |
            | successfully acknowledged |

    Scenario Outline: acknowledge with invalid guild
        Given guild has not been initialized
        When acknowledge
        Then bot sends <output>

        Examples:
            | output               |
            | guild not registered |
