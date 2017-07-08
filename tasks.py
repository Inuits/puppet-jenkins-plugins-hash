"""Invoke tasks."""
import glob
from invoke import task


@task(
    aliases=["flake8", "pep8"],
    help={
        'filename': 'File(s) to lint. Supports globbing.',
    },
)
def lint(ctx, filename=None):
    """Run flake8 python linter."""
    command = 'flake8'
    if filename is not None:
        files = [x for x in glob.glob(filename)]
        command += ' ' + " ".join(files)

    ctx.run(command)
