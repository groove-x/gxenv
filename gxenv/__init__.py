import os
import pathlib
import shutil
import subprocess
import sys
import textwrap
import traceback
import venv

from glob import glob

import gxenv.const


def _printerr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def fmt_env_path(env_name, *dirs):
    """Construct directory path.

    Args:
        env_name: name of an env.
        *dirs: trailing directories after env name.

    Returns:
        str: concatenated directory path.
    """

    p = pathlib.Path(const.env_base) / env_name
    for a in dirs:
        p /= a
    return str(p)


def check_env_exists(env_name, verbose=False):
    """Checks if the specified env exists in envs directory.

    Args:
        env_name: name of an env.
        verbose: if True, it becomes verbose

    Raises:
        NotADirectoryError: there's a file of name, not directory.
    """

    if verbose:
        _printerr(
            'gxenv check_env_exists: checking if env "{}" exists'.format(env_name)
        )

    env_dir = fmt_env_path(env_name)
    if not os.path.exists(env_dir):
        if verbose:
            _printerr(
                'gxenv check_env_exists: env "{}" does not exist'.format(env_name)
            )
        raise FileNotFoundError('Specified env "{}" does not exist'.format(env_name))

    if not os.path.isdir(env_dir):
        if verbose:
            _printerr(
                'gxenv check_env_exists: file named "{}" exists but is not a directory'.format(
                    env_name
                )
            )
        raise NotADirectoryError('Non-directory file is at "{}"'.format(env_dir))

    if verbose:
        _printerr(
            'gxenv check_env_exists: env "{}" exists at "{}"'.format(env_name, env_dir)
        )


def run(env_name: str, executable_name: str, argv, verbose=False):
    """Inner run function.

    Args:
        env_name: name of env.
        executable_name: name of exectable.
        verbose: if True, it becomes verbose.
        argv: args for the executable.
    """

    if verbose:
        print('original argv:', sys.argv)
        print('executable_name:', executable_name)

    check_env_exists(env_name, verbose=verbose)
    found = which(env_name, executable_name, verbose=verbose)
    if found is None:
        raise FileNotFoundError(
            "Executable {} was not found in env {}".format(executable_name, env_name)
        )

    argv.insert(0, found)

    if verbose:
        print('new argv:', argv)

    os.execv(found, argv)


def cmd_run(env_name: str, executable_name: str, verbose=False, meta=None):
    """Run specified command in the env.

    Args:
        env_name: name of env.
        executable_name: name of executable.
        verbose: if True, it becomes verbose.
        meta: a dict which will contain 'argv: [arg1, arg2, ...]' as an item.
    """

    argv = meta.get('argv', [])

    '''
    if executable_name.startswith('python'):
        argv.insert(0, '-')
    '''

    run(env_name, executable_name, argv, verbose)


def cmd_create(env_name: str, verbose=False):
    """Create new env.

    The env is to be created in /var/lib/python3/envs/ by venv.

    Args:
        env_name: name of new env.
        verbose: if True, it becomes verbose
    """

    path = fmt_env_path(env_name)

    if verbose:
        _printerr('gxenv create: "{}" at "{}"'.format(env_name, path))

    venv.create(
        path, system_site_packages=False, clear=False, symlinks=True, with_pip=True
    )

    if verbose:
        _printerr('gxenv create: successfully created env "{}"'.format(env_name))


def cmd_list(verbose=False):
    """List all envs.

    Args:
        verbose: if True, it becomes verbose
    """

    query = fmt_env_path("*")

    if verbose:
        _printerr(
            'gxenv list: finding envs in "{}" by glob, query = "{}"'.format(
                const.env_base, query
            )
        )

    dirs = glob(query)
    print("\n".join(dirs))


def cmd_purge(env_name: str, force=False, verbose=False):
    """Remove an env.

    Args:
        env_name: name of an env
        force: True if it shouldn't raise when the specified env does not exist.
        verbose: if True, it becomes verbose
    """

    try:
        check_env_exists(env_name, verbose=verbose)
    except FileNotFoundError as e:
        if not force:
            raise e
        return

    def onerror(fn, path, exc_info):
        s = """
            Could not purge the env {env_name}\n
            Full path: {path}
            Function: {func}
            """

        print(
            textwrap.dedent(s)
            .strip()
            .format(env_name=env_name, path=path, func=fn.__name__),
            end="\n\n",
        )
        traceback.print_exception(*exc_info)

    env_dir = fmt_env_path(env_name)

    if verbose:
        _printerr('gxenv purge: remove env "{}" at "{}"'.format(env_name, env_dir))

    shutil.rmtree(env_dir, ignore_errors=False, onerror=onerror)

    if verbose:
        _printerr(
            'gxenv purge: successfully removed env "{}" at "{}"'.format(
                env_name, env_dir
            )
        )


def which(env_name, executable_name, verbose=True):
    """Inner which function for testability/convenience.

    Args:
        env_name: name of env.
        executable_name: name of executable that we want to find.
        verbose: if True, it becomes verbose

    Returns:
        Optional[str]: full path of found executable if it's found, None otherwise.

    """

    env_dir = fmt_env_path(env_name, "bin")
    if verbose:
        _printerr(
            'gxenv which: finding "{}" in env "{}"'.format(executable_name, env_name)
        )

    found = shutil.which(executable_name, path=env_dir)

    if verbose:
        _printerr(
            'gxenv which: "{}" was found in env "{}" at "{}"'.format(
                executable_name, env_name, found
            )
        )

    return found


def cmd_which(env_name: str, executable_name, verbose=False):
    """Show where given exec exists.

    Args:
        env_name: name of env.
        executable_name: name of executable.
        verbose: if True, it becomes verbose
    """

    check_env_exists(env_name, verbose=verbose)
    found = which(env_name, executable_name, verbose=verbose)
    if found is None:
        raise FileNotFoundError(
            "Executable {} was not found in env {}".format(executable_name, env_name)
        )

    print(found)
