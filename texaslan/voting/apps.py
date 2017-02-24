from django.apps import AppConfig


class VotingConfig(AppConfig):
    name = 'texaslan.voting'
    verbose_name = "Voting"

    def ready(self):
        """Override this to put in:
        """
        pass
