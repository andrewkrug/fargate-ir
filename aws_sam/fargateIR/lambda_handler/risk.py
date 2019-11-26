"""Map guardDuty finding to risk levels for our environment."""


class Finding(object):
    def __init__(self, finding):
        self.finding = finding

    def risk_level(self):
        """Classify finding on the standard risk scale."""

        DEFAULT_FINDING_LEVEL = "LOW"

        level_map = {
            "UnauthorizedAccess:EC2/SSHBruteForce": "LOW",
            "UnauthorizedAccess:EC2/RDPBruteForce": "LOW",
            "Recon:EC2/Portscan": "HIGH",
            "Custom:UserReport/WebsiteDefacement": "MAXIMUM",
        }

        return level_map.get(self.finding["detail"]["type"], DEFAULT_FINDING_LEVEL)
