"""Credentials class for HashiCorp Vault passwords."""
import os
import hvac

from django.conf import settings
from .nautobot_orm import MixinNautobotORMCredentials

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["nautobot_plugin_nornir"]


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

        self.url = PLUGIN_SETTINGS.get("vault_url", os.environ["VAULT_ADDR"])
        # Namespace is optional
        self.namespace = PLUGIN_SETTINGS.get("vault_namespace", os.getenv("VAULT_NAMESPACE"))
        self.role_id = PLUGIN_SETTINGS.get("vault_role_id", os.environ["VAULT_ROLE_ID"])
        self.secret_id = PLUGIN_SETTINGS.get("vault_secret_id", os.environ["VAULT_SECRET_ID"])
        self.nautobot_secret_path = PLUGIN_SETTINGS.get("nautobot_secret_path", os.environ["NAUTOBOT_SECRET_PATH"])
        self.client = hvac.Client(
            url=self.url, role_id=self.role_id, secret_id=self.secret_id, namespace=self.namespace
        )

        self.secrets = self.client.secrets.kv.read_secret_version(path=self.nautobot_secret_path)
        self.creds = self.secrets["data"]["data"]

        self.username = self.creds["username"]
        self.password = self.creds["password"]
        self.secret = self.creds.get("secret", self.password)
