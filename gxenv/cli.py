import argparse

import gxenv


class SugoiArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, short_description=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.short_description = short_description

        self.replace_arg_group_description("positional arguments", "commands")
        self.replace_arg_group_description("optional arguments", "options")

    # Add brief message before usage by overriding format_help
    def format_help(self):
        if self.short_description is not None:
            self._print_message(self.short_description + "\n")
        self._print_message(super().format_help())

    def replace_arg_group_description(self, old_desc, new_desc):
        for ag in self._action_groups:
            if ag.title.startswith(old_desc):
                ag.title = new_desc


def expand_arg(func):
    def inner(args, meta=None):
        # `meta` is an optional dict to pass objects to func
        # regardless of parsed args.
        filtered = {k: v for k, v in vars(args).items() if not k.endswith("_")}
        if meta:
            func(**filtered, meta=meta)
        else:
            func(**filtered)

    return inner


def create_argparse_instance():
    root = SugoiArgumentParser(
        prog="gxenv", short_description="gxenv - a GX-flavored venv wrapper"
    )
    root.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="enable verbose output",
    )
    subparsers = root.add_subparsers()

    sub_create = subparsers.add_parser("create", help="create an env")
    sub_create.add_argument("env_name", help="name of new env")
    sub_create.set_defaults(run_=expand_arg(gxenv.cmd_create))

    sub_list = subparsers.add_parser("list", help="list envs")
    sub_list.set_defaults(run_=expand_arg(gxenv.cmd_list))

    sub_purge = subparsers.add_parser("purge", help="delete an env")
    sub_purge.add_argument("env_name", help="name of env")
    sub_purge.set_defaults(run_=expand_arg(gxenv.cmd_purge))

    sub_which = subparsers.add_parser(
        "which", help="find specified executable in an env"
    )
    sub_which.add_argument("env_name", help="name of env")
    sub_which.add_argument("executable_name", help="name of executable")
    sub_which.set_defaults(run_=expand_arg(gxenv.cmd_which))

    sub_run = subparsers.add_parser("run", help="run an executable in an env")
    sub_run.add_argument("env_name", help="name of env")
    sub_run.add_argument("executable_name", help="name of executable")
    sub_run.set_defaults(run_=expand_arg(gxenv.cmd_run))

    return root
