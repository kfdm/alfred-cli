import glob
import logging
import os
import plistlib
import subprocess
import zipfile

import click


logger = logging.getLogger(__name__)

project_root = os.path.realpath('.')
project_name = os.path.basename(project_root)
archive_path = os.path.join(project_root, project_name + '.alfredworkflow')


@click.group()
@click.option('-v', '--verbose', count=True)
def main(verbose):
    logging.basicConfig(level=(logging.WARNING - 10 * verbose))


@main.command()
def build():
    '''Build Alfred Extension'''
    logger.info('Reading %s', project_root)
    logger.info('Building %s', project_name)

    with zipfile.ZipFile(archive_path, 'a') as zfp:
        # git-ls-files will let us take advantage of .gitignore to ignore
        # files that we do not want to save in our extension
        for path in subprocess.check_output(['git', 'ls-files']).strip().split('\n'):
            logger.info('Adding %s', path)
            zfp.write(path, os.path.basename(path))

    click.echo('Built workflow ' + archive_path)


@main.command()
@click.pass_context
def open(ctx):
    '''Open Alfred Extension in Alfred'''
    ctx.forward(build)
    click.launch(archive_path)


@main.command()
def list():
    click.echo('Listing alfred extensions')

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
        plist = plistlib.readPlist(path)
        print 'Name:', plist.get('name')
        print 'Description', plist.get('description')
        print 'BundleID', plist.get('bundleid')
        print 'Category', plist.get('category')
        print 'Creator', plist.get('createdby')
        print 'URL', plist.get('webaddress')
        print 'Path', path
        print 
