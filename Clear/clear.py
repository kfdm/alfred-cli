import logging
import os
import subprocess

logger = logging.getLogger(__name__)

BASE = os.path.dirname(__file__)
SETTINGS = os.path.join(
    os.path.expanduser('~'),
    'Library',
    'Application Support',
    'Alfred 2',
    'Workflow Data',
    'net.kungfudiscomonkey.alfred.clear',
)
WHITELIST = os.path.join(SETTINGS, 'whitelist.txt')
try:
    with open(os.path.join(BASE, 'icon.png')) as fp:
        ICON = fp.read()
except:
    ICON = None

try:
    from gntp.config import mini
except:
    def mini(message, **kwargs):
        print message


class Clear(object):
    def message(self, message):
        mini(message, applicationName='Clear', applicationIcon=ICON)

    def _run(self, script):
        p = subprocess.Popen(
            ['osascript'],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        out, err = p.communicate(script)

        if err:
            logger.warn(err)

        return out.strip()

    def _write(self, whitelist):
        with open(WHITELIST, 'w') as fp:
            fp.write('\n'.join(whitelist))

    def current_processes(self):
        processes = set(self._run("""
            tell application "System Events" to set the visible of every process to true
            tell application "Finder" to get the name of every process whose visible is true
            """).split(', '))
        processes.remove('Finder')
        return processes

    def kill(self, app):
        mini('Killing {0}'.format(app))
        return self._run("""
            tell application "{0}" to quit
            """.format(app))

    def get_whitelist(self):
        if not os.path.exists(WHITELIST):
            return set(['Finder'])
        with open(WHITELIST) as fp:
            whitelist = set(fp.read().strip().split('\n'))
            whitelist.add('Finder')
        return whitelist

    def add_whitelist(self, value):
        print 'Adding', value, 'to whitelist'
        if not os.path.exists(SETTINGS):
            logger.info('Creating settings directory: %s', SETTINGS)
            os.makedirs(SETTINGS)
        whitelist = self.get_whitelist()
        whitelist.add(value)
        self._write(whitelist)

    def del_whitelist(self, value):
        print 'Removing', value, 'from whitelist'
        if not os.path.exists(SETTINGS):
            return
        whitelist = self.get_whitelist()
        whitelist.remove(value)
        self._write(whitelist)

    def run(self):
        whitelist = self.get_whitelist()
        processes = self.current_processes()
        logger.debug('Using whitelist: %s', whitelist)
        logger.debug('Currently running: %s', processes)
        for app in processes:
            if app in whitelist:
                logger.info('Skipping %s', app)
            else:
                self.kill(app)

    def xml(self):
        print '<?xml version="1.0"?>'
        print '<items>'
        for item in self.current_processes():
            print '<item uid="{0}" arg="{1}">'.format(item, item)
            print '<title>{0}</title>'.format(item)
            print '</item>'
        print '</items>'

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    c = Clear()
    c.run()
