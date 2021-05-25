"""Credentials class for HashiCorp Vault passwords."""
from .nautobot_orm import MixinNautobotORMCredentials

class HashiCorpVaultVars(MixinNautobotORMCredentials):
    """Credentials Class designed to work with Nautobot ORM.

    This class supports retrieving username/password/secret keys from path(s) in HashiCorp Vault.

    Args:
        NautobotORMCredentials ([type]): [description]
    """

    def __init__(self, params=None):
        """Initialize Credentials Class designed to work with Nautobot ORM.

        Args:
            params ([dict], optional): Credentials Parameters
        """
        if not params:
            params = {}

        if not isinstance(params, dict):
            raise TypeError("params must be a dictionnary")

        self.username = ""
        self.password = ""
        self.secret = ""