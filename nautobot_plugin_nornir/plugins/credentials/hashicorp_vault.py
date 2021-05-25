"""Credentials class for HashiCorp Vault passwords."""
import os
import hvac

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
            raise TypeError("params must be a dictionary")

        self.username = ""
        self.password = ""
        self.secret = ""

        self.url = params.get("vault_url", os.environ["VAULT_ADDR"])
        # Namespace is optional
        self.namespace = params.get("vault_namespace", os.getenv("VAULT_NAMESPACE"))
        self.role_id = params.get("vault_role_id", os.environ["VAULT_ROLE_ID"])
        self.secret_id = params.get("vault_secret_id", os.environ["VAULT_SECRET_ID"])
        self.client = hvac.Client(
            url=self.url, role_id=self.role_id, secret_id=self.secret_id, namespace=self.namespace
        )
