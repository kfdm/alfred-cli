import shutil
import logging
import os
import plistlib
import subprocess
import zipfile

import click

import alfredcli.util


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
def install(ctx):
    '''Open Alfred Extension in Alfred'''
    ctx.forward(build)
    click.launch(archive_path)


@main.command()
@click.option('-f', '--full', is_flag=True)
def list(full):
    click.echo('Listing alfred extensions')
    click.echo('-' * 80)

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

    for path, plist in alfredcli.util.workflows():
        print plist.get('name'),
        print '[', plist.get('bundleid'), ']'
        if full:
            print 'Description', plist.get('description')
            print 'Category', plist.get('category')
            print 'Creator', plist.get('createdby')
            print 'URL', plist.get('webaddress')
            print 'Path', path
            print


@main.command(name='import')
@click.argument('bundleid')
def import_(bundleid):
    for path, plist in alfredcli.util.workflows():
        if plist.get('bundleid') == bundleid:
            break
    else:
        click.fail('Unable to find bundle id: {0}'.format(bundleid))

    source_dir = os.path.dirname(path)
    dest_dir = os.getcwd()
    click.echo('Importing {0} from {1} to {2}'.format(bundleid, source_dir, dest_dir))

    for root, dirs, files in os.walk(source_dir):
        for f in files:
            if f != 'info.plist':
               continue
            source_path = os.path.join(root, f)
            dest_path = os.path.join(dest_dir, f)
            click.echo('Copying {0} to {1}'.format(source_path, dest_path))
            shutil.copy(source_path, dest_path)


@main.command()
def info():
    import pprint
    plist = plistlib.readPlist('info.plist')
    print 'Name:', plist.get('name')
    print 'Description', plist.get('description')
    print 'BundleID', plist.get('bundleid')
    print 'Category', plist.get('category')
    print 'Creator', plist.get('createdby')
    print 'URL', plist.get('webaddress')
    pprint.pprint(plist)
    print 
