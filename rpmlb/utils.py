"""Utilify module."""

import importlib
import logging
import os
import subprocess
import sys
from contextlib import contextmanager

LOG = logging.getLogger(__name__)


def p(text):
    """Print object's dump information.

    Such as Perl's Data::Dumper, Ruby's p method, PHP's var_dump method.
    """
    print(repr(text))


def camelize(word):
    """Convert the word from snake case (foo_bar) to camel case (FooBar)."""
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def get_class(class_name: str, package: str = __package__):
    """Dynamically import class from a module.

    Keyword arguments:
        class_name: The class/attribute name in standard import form.
        package: Name of the package to import from (for relative imports).

    Returns:
        type: The requested class.

    """
    mod_name, class_name = class_name.rsplit(sep='.', maxsplit=1)
    module = importlib.import_module(mod_name, package)
    return getattr(module, class_name)


def get_instance(class_name: str, *args, **kwargs):
    """Dynamically instantiate a class.

    Keyword arguments:
        class_name: Absolute or relative import name of the class.
        *args: Positional arguments for the class __init__.
        **kwargs: Keyword arguments for the class __init__.

    Return:
        Instance of the specified class.

    """
    cls = get_class(class_name)
    return cls(*args, **kwargs)


@contextmanager
def pushd(new_dir):
    """Behave like a shell command "pushd new_dir; popd".

    Change directory to new_dir, do something, then change back
    to previous directory.
    """
    previous_dir = os.getcwd()
    try:
        new_ab_dir = None
        if not os.path.isabs(new_dir):
            new_ab_dir = os.path.join(previous_dir, new_dir)
        else:
            new_ab_dir = new_dir
        # Use absolute path to show it on FileNotFoundError message.
        os.chdir(new_ab_dir)
        yield
    finally:
        os.chdir(previous_dir)


def run_cmd_with_capture(cmd, **kwargs):
    """Run command captureing stdout and stdin.

    The captured value is saved in the return value.
    """
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    return run_cmd(cmd, **kwargs)


def run_cmd(cmd, **kwargs):
    """Run shell command with subprocess module.

    Environment variables are inherited into the shell command's environment.
    If the log level is debug, the command line is outputted as a log.
    """
    returncode = None
    stdout = ''
    stderr = ''
    proc = None
    try:
        check = True
        if 'check' in kwargs:
            check = kwargs['check']
            kwargs.pop('check', None)
        # Use shell option to use wildcard "*".
        kwargs['shell'] = True

        LOG.debug('CMD: %s, kwargs: %s', cmd, repr(kwargs))

        env = os.environ.copy()
        env['LC_ALL'] = 'en_US.utf-8'  # better to parse English output
        if 'env' in kwargs:
            env.update(kwargs['env'])
        kwargs['env'] = env

        proc = subprocess.Popen(cmd, **kwargs)
        stdout, stderr = proc.communicate()
        returncode = proc.returncode
        if check and returncode != 0:
            LOG.error('CMD: [%s] failed at [%s]', cmd, os.getcwd())
            LOG.error('Return Code: %s', returncode)
            if stdout is not None:
                LOG.error('Stdout: %s', stdout)
            if stderr is not None:
                LOG.error('Stderr: %s', stderr)

            kwargs_dict = {}
            kwargs_dict['output'] = stdout
            if sys.version_info >= (3, 5):
                kwargs_dict['stderr'] = stderr
            raise subprocess.CalledProcessError(
                returncode, cmd, **kwargs_dict
            )
        return CompletedProcess(cmd, returncode, stdout, stderr)
    except Exception as e:
        try:
            proc.kill()
        except:
            pass
        raise e


class CompletedProcess:
    """A error class to manage the result of command.

    Use it instead of subprocess.CompletedProcess/CalledProcessError
    for old Pytyons (<= 3.4).
    """

    def __init__(self, cmd, returncode, stdout, stderr):
        """Initialize this class."""
        self.cmd = cmd
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
