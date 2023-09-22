from . import get_default_config, apply_settings


config = get_default_config()
config["pipeline"] = {
    "Cache": {},
    "DDragon": {},
    "RiotAPI": {
        "api_key": "RIOT_API_KEY",
        "request_error_handling": {
            "404": {"strategy": "throw"},
            "429": {
                "service": {
                    "strategy": "exponential_backoff",
                    "initial_backoff": 1.0,
                    "backoff_factor": 2.0,
                    "max_attempts": 4,
                },
                "method": {"strategy": "retry_from_headers", "max_attempts": 5},
                "application": {"strategy": "retry_from_headers", "max_attempts": 5},
            },
            "500": {
                "strategy": "exponential_backoff",
                "initial_backoff": 1.0,
                "backoff_factor": 2.0,
                "max_attempts": 4,
            },
            "503": {
                "strategy": "exponential_backoff",
                "initial_backoff": 1.0,
                "backoff_factor": 2.0,
                "max_attempts": 8,
            },
            "timeout": {"strategy": "throw"},
            "403": {"strategy": "throw"},
            "504": {
                "strategy": "exponential_backoff",
                "initial_backoff": 1.0,
                "backoff_factor": 2.0,
                "max_attempts": 4,
            },
            "502": {
                "strategy": "exponential_backoff",
                "initial_backoff": 1.0,
                "backoff_factor": 2.0,
                "max_attempts": 4,
            },
        },
    },
}

# config["global"]["version_from_match"] = "latest"
# config["logging"]["print_calls"] = False
config["logging"]["print_riot_api_key"] = True
apply_settings(config)
