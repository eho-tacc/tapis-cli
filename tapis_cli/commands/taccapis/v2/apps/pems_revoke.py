from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import Username
from .mixins import AppIdentifier
from tapis_cli.commands.taccapis.model import Permission

from . import API_NAME, SERVICE_VERSION
from .formatters import AppsFormatMany

__all__ = ['AppsPemsRevoke']


class AppsPemsRevoke(AppsFormatMany, AppIdentifier, Username):

    HELP_STRING = 'Revoke Permissions on an App for a User'
    LEGACY_COMMMAND_STRING = 'apps-pems-update'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(AppsPemsRevoke, self).get_parser(prog_name)
        parser = AppIdentifier.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        app_id = AppIdentifier.get_identifier(self, parsed_args)

        body = {'username': parsed_args.username, 'permission': 'NONE'}
        headers = self.render_headers(Permission, parsed_args)
        revoke_result = self.tapis_client.apps.updateApplicationPermissions(
            appId=app_id, body=body)
        results = self.tapis_client.apps.listPermissions(appId=app_id)

        records = []
        for rec in results:
            record = []
            # Table display
            if self.app_verbose_level > self.VERBOSITY:
                record.append(rec.get('username'))
                record.extend(Permission.pem_to_row(rec.get('permission', {})))
            else:
                for key in headers:
                    val = self.render_value(rec.get(key, None))
                    record.append(val)
            # Deal with an API-side bug where >1 identical pems are
            # returned for the owning user when no additional pems have been
            # granted on the app
            if record not in records:
                records.append(record)

        return (tuple(headers), tuple(records))
