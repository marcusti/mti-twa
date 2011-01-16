#-*- coding: utf-8 -*-

from members.csvutf8 import UnicodeReader, UnicodeWriter
from operator import itemgetter
import os, sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'exit. no file specified.'
        sys.exit(2)

    filename = sys.argv[1]
    if not os.path.exists(filename) or not os.path.isfile(filename):
        print 'exit. file does not exist: %s' % filename
        sys.exit(2)

    content = []
    header = None

    print 'reading file %s' % filename
    with open(filename) as f:
        for i, line in enumerate(UnicodeReader(f)):
            if i == 0:
                header = line
            else:
                content.append(line)

    print 'sorting'
    content.sort(key=itemgetter(header.index('LASTNAME')))
    content.sort(key=itemgetter(header.index('FIRSTNAME')))
    content.sort(key=itemgetter(header.index('DOJO')))
    content.sort(key=itemgetter(header.index('DOJO CITY')))
    content.sort(key=itemgetter(header.index('DOJO COUNTRY')))

    path, name = os.path.split(filename)
    filename_base, filename_ext = os.path.splitext(name)
    filename_out = os.path.join(path, filename_base + '-sorted' + filename_ext)

    print 'writing %s' % filename_out
    with open(filename_out, 'w') as f:
        writer = UnicodeWriter(f)
        writer.writerow(header)
        for line in content:
            writer.writerow(line)
