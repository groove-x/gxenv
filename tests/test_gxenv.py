import os
import shutil
import subprocess
import unittest

import gxenv
from gxenv import const


class GxenvTest(unittest.TestCase):
    env_dir = gxenv.fmt_env_path(const.test_env_name)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.longMessage = True

    def test_existence_check(self):
        if os.path.exists(self.env_dir):
            shutil.rmtree(self.env_dir)

        # 1. env does not exist
        with self.assertRaises(FileNotFoundError):
            gxenv.check_env_exists(const.test_env_name, verbose=True)

        # 2. env exists
        os.mkdir(self.env_dir)
        gxenv.check_env_exists(const.test_env_name, verbose=True)
        os.rmdir(self.env_dir)

        # 3. raise if env_path is not a dir
        with open(self.env_dir, "w"):
            # just make a blank file
            pass

        with self.assertRaises(NotADirectoryError):
            gxenv.check_env_exists(const.test_env_name, verbose=True)

    def test_create_and_purge(self):
        # 1. env shouldn't exist for now
        with self.assertRaises(FileNotFoundError):
            gxenv.check_env_exists(const.test_env_name, verbose=True)

        # 2. create env and check if the created env exists
        gxenv.cmd_create(const.test_env_name, verbose=True)

        # 3. purge env
        gxenv.cmd_purge(const.test_env_name, force=False, verbose=True)

        # 4. raise when purging non-existent env
        with self.assertRaises(FileNotFoundError):
            gxenv.cmd_purge(const.test_env_name, force=False, verbose=True)

        # 5. no raise when force option is True
        gxenv.cmd_purge(const.test_env_name, force=True, verbose=True)

    def test_which(self):
        # 1. create env
        gxenv.cmd_create(const.test_env_name, verbose=True)

        # 2. ensure found `python` is identical to ideal one
        exec_gxenv = gxenv.which(const.test_env_name, "python", verbose=True)
        exec_ideal = gxenv.fmt_env_path(const.test_env_name, "bin", "python")
        self.assertEqual(exec_gxenv, exec_ideal)

        # 3. ensure found `pip` is identical to ideal one by path
        exec_gxenv = gxenv.which(const.test_env_name, "pip", verbose=True)
        exec_ideal = gxenv.fmt_env_path(const.test_env_name, "bin", "pip")
        self.assertEqual(exec_gxenv, exec_ideal)

        # 4. ensure found `pip` is identical to ideal one by -V output
        out_gxenv = subprocess.check_output([exec_gxenv, "-V"])
        out_ideal = subprocess.check_output([exec_ideal, "-V"])
        self.assertEqual(out_gxenv, out_ideal)

    def test_env_integrity(self):
        gxenv.cmd_create(const.test_env_name, verbose=True)

        # 1. find commands
        for executable in ["python", "python3", "pip", "pip3"]:
            found = gxenv.which(const.test_env_name, executable, verbose=True)
            if found is None:
                raise FileNotFoundError(
                    "executable `{}` was not found".format(executable)
                )

    @classmethod
    def tearDown(cls):
        if os.path.exists(cls.env_dir):
            if os.path.isdir(cls.env_dir):
                shutil.rmtree(cls.env_dir, ignore_errors=True)
            else:
                os.remove(cls.env_dir)
