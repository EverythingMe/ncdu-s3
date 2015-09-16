from __future__ import absolute_import

import time
import ujson as json


class NcduDataWriter(object):
    """
    Write ncdu formatted data files (like ncdu -o)

    I couldn't find any good streaming JSON writers for python, so this is a bit hackish, but safe.
    All JSON objects are written with json.dump(), the only stuff I write directly to the file are
    ints, newlines, commas and square brackets
    """

    def __init__(self, output, root):
        """
        :type output: io.RawIOBase
        :type root: str
        """

        self.output = output
        self.depth = 0

        self.output.write('[1,0,')
        json.dump({'progname': 'ncdu-s3', 'progver': '0.1', 'timestamp': int(time.time())}, self.output)

        # ncdu data format must begin with a directory
        self.dir_enter(root)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def dir_enter(self, name):
        """
        :type name: str
        """

        self.depth += 1

        self.output.write(",\n")

        self.output.write('[')
        json.dump({'name': name}, self.output)

    def dir_leave(self):
        if self.depth > 0:
            self.depth -= 1
            self.output.write(']')

    def file_entry(self, name, size):
        """
        :type name: str
        :type size: int
        """

        self.output.write(",\n")

        json.dump({'name': name, 'dsize': size}, self.output)

    def close(self):
        for i in xrange(self.depth):
            self.dir_leave()

        # close the format JSON document we opened in our constructor
        self.output.write(']')