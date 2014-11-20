import logging
import os
import subprocess
import sys
import workflow

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

    def __call__(self, wf):
        if 'whitelist' not in wf.settings:
            wf.settings['whitelist'] = ['Finder']

        if wf.args[0] == 'whitelist':
            return self.add_whitelist(wf, wf.args[1])
        elif wf.args[0] == 'blacklist':
            return self.del_whitelist(wf, wf.args[1])
        elif wf.args[0] == 'run':
            return self.run(wf)
        elif wf.args[0] == 'list':
            for item in self.current_processes():
                icon = workflow.ICON_BURN \
                    if item in wf.settings['whitelist'] \
                    else workflow.ICON_FAVORITE
                wf.add_item(item, arg=item, valid=True, icon=icon)
            wf.send_feedback()
        else:
            wf.add_item('No items', icon=workflow.ICON_WARNING)
            wf.send_feedback()

    def add_whitelist(self, wf, item):
        if item in wf.settings['whitelist']:
            print item, 'already whitelisted'
            return
        wf.settings['whitelist'].append(item)
        print 'Whitelisted', item
        wf.settings.save()

    def del_whitelist(self, wf, item):
        if item in wf.settings['whitelist']:
            wf.settings['whitelist'].remove(item)
            print 'Blacklisted', item
            wf.settings.save()

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

    def run(self, wf):
        whitelist = wf.settings['whitelist']
        processes = self.current_processes()
        wf.logger.debug('Using whitelist: %s', whitelist)
        wf.logger.debug('Currently running: %s', processes)
        for app in processes:
            if app in whitelist:
                wf.logger.info('Skipping %s', app)
            else:
                self.kill(app)

if __name__ == '__main__':
    sys.exit(workflow.Workflow().run(Clear()))
