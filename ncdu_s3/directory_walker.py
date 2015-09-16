from __future__ import absolute_import

import itertools


class DirectoryWalker(object):
    def __init__(self, writer):
        """
        :type writer: ncdu_s3.NcduDataWriter
        """

        self.writer = writer
        self.current_path = []

    def process_item(self, path, size):
        key_filename = path.pop()

        if self.current_path != path:
            # update our position in the directory hierarchy
            conflict = False
            add_dirs = []

            for p1, p2 in itertools.izip_longest(self.current_path, path):
                if p1 != p2:
                    # first conflict starts another logic in our code
                    conflict = True

                if conflict:
                    if p1 is not None:
                        self.writer.dir_leave()

                    if p2 is not None:
                        add_dirs.append(p2)

            for d in add_dirs:
                # ncdu doesn't support empty dir names. Replace '' with '<empty>'
                self.writer.dir_enter(d if d != '' else '<empty>')

            self.current_path = path

        # directory entry ends with a '/' so the key_filename will be ''.
        # in that case, omit it
        if key_filename != '':
            self.writer.file_entry(key_filename, size)
