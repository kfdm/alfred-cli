import glob
import logging
import os
import plistlib
import subprocess

logger = logging.getLogger(__name__)


def workflows():
    sync_folder = subprocess.check_output([
        'defaults',
        'read',
        'com.runningwithcrayons.Alfred-Preferences',
        'syncfolder'
    ]).strip()
    logger.info('Sync Folder: %s', sync_folder)
    workflow_glob = os.path.join(
        os.path.expanduser(sync_folder),
        'Alfred.alfredpreferences',
        'workflows',
        '**',
        'info.plist',
    )
    logger.info('Search Glob: %s', workflow_glob)

    for path in glob.iglob(workflow_glob):
        yield path, plistlib.readPlist(path)


def data_dir(bundleid):
    return os.path.join(
        os.path.expanduser('~'),
        'Library',
        'Application Support',
        'Alfred 2',
        'Workflow Data',
        bundleid
    )


def cache_dir(bundleid):
    return os.path.join(
        os.path.expanduser('~'),
        'Library',
        'Caches',
        'com.runningwithcrayons.Alfred-2',
        'Workflow Data',
        bundleid
    )


def workflow_plist():
    return plistlib.readPlist('info.plist')
