from __future__ import absolute_import
import click
import itertools
import urlparse
from ncdu_s3 import NcduDataWriter, DirectoryWalker, S3DirectoryGenerator


@click.command()
@click.argument('s3-url')
@click.argument('output', type=click.File('w'))
@click.pass_context
def main(ctx, s3_url, output):
    assert isinstance(ctx, click.Context)

    try:
        s3_directory_generator = S3DirectoryGenerator(s3_url)
    except SyntaxError, e:
        ctx.fail(e.message)
        return

    with NcduDataWriter(output, s3_url) as ncdu:
        walker = DirectoryWalker(ncdu)

        for path, size in s3_directory_generator:
            walker.process_item(path, size)

if __name__ == '__main__':
    main()
