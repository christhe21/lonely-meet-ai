"""
Central orchestrator / state machine.

States (planned):
- IDLE
- JOINING
- STANDING_BY
- LISTENING
- THINKING
- SPEAKING
- ERROR
"""

class Orchestrator:
    def __init__(self):
        pass

    async def run(self):
        raise NotImplementedError("Orchestrator not yet implemented")
