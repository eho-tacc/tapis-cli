import os
from tapis_cli.clients.services.mixins import JobsUUID, RemoteFilePath
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from ..files.models import File
from ..files.formatters import FilesFormatOne
from .helpers.sync import download

__all__ = ['JobsOutputsDownload']


class JobsOutputsDownload(FilesFormatOne, JobsUUID, RemoteFilePath):
    """Download a jobs output file or directory
    """

    # TODO - add --cwd option to disable creating job folder
    def get_parser(self, prog_name):
        parser = FilesFormatOne.get_parser(self, prog_name)
        parser = JobsUUID.extend_parser(self, parser)
        parser = RemoteFilePath.extend_parser(self, parser)
        parser.add_argument(
            '--cwd',
            dest='use_cwd',
            action='store_true',
            help="Download to '.' instead of a job-specific subdirectory")
        syncmode = parser.add_mutually_exclusive_group(required=False)
        syncmode.add_argument('--force',
                              dest='overwrite',
                              action='store_true',
                              help='Always overwrite existing files')
        syncmode.add_argument(
            '--sync',
            dest='sync',
            action='store_true',
            help='Overwrite only when timestamp or size differs')
        # parser.add_argument('--atomic',
        #                     dest='atomic',
        #                     action='store_true',
        #                     help='Download atomically')
        parser.add_argument('--progress',
                            dest='progress',
                            action='store_true',
                            help='Report progress to STDERR')
        parser.add_argument('--exclude',
                            nargs='+',
                            metavar='filename',
                            help='One or more files to exclude from download')
        parser.add_argument('--include',
                            nargs='+',
                            metavar='filename',
                            help='One or more files to include')
        return parser

    def take_action(self, parsed_args):
        parsed_args = FilesFormatOne.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        # Optionally disable creation and use of a job folder
        dest_dir = './{0}'.format(parsed_args.job_uuid)
        if parsed_args.use_cwd:
            dest_dir = '.'
        else:
            os.makedirs(dest_dir, exist_ok=True)

        headers = SearchableCommand.headers(self, File, parsed_args)
        downloaded, skipped, exceptions, elapsed = download(
            parsed_args.file_path,
            parsed_args.job_uuid,
            destination=dest_dir,
            excludes=parsed_args.exclude,
            includes=parsed_args.include,
            force=parsed_args.overwrite,
            sync=parsed_args.sync,
            progress=parsed_args.progress,
            atomic=False,
            agave=self.tapis_client)

        headers = ['downloaded', 'skipped', 'warnings', 'elapsed_sec']
        if parsed_args.formatter in ('json', 'yaml'):
            data = [downloaded, skipped, [str(e) for e in exceptions], elapsed]
        else:
            data = [len(downloaded), len(skipped), len(exceptions), elapsed]
        return (tuple(headers), tuple(data))
