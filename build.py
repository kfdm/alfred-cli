#!/usr/bin/env python2.7
import os
import glob
import subprocess
import zipfile
import collections


PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

# Do everything relative to the project root
os.chdir(PROJECT_ROOT)

extensions = collections.defaultdict(list)

# git-ls-files will let us take advantage of .gitignore to ignore
# files that we do not want to save in our extension
for path in subprocess.check_output(['git', 'ls-files']).split('\n'):
    try:
        foldername, filename = path.split('/', 1)
    except ValueError:
        continue
    else:
        extensions[foldername].append(path)

for extension in extensions:
    archive_path = os.path.join(PROJECT_ROOT, extension + '.alfredworkflow')
    with zipfile.ZipFile(archive_path, 'a') as zfp:
        print 'Building extension:', extension
        for f in extensions[extension]:
            print 'Adding', f
            zfp.write(f, os.path.basename(f))
