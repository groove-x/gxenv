gxenv
=====

*A venv wrapper to manage envs in one place, with a convenient CLI.*


How to use
----------

Plain `venv` does not provide how to manage envs exist in the system.

Gxenv provides you a simple CLI to:

 - Create env
 - List envs
 - Purge envs
 - Find an executable in an env
 - Run an executable in an env with arguments

Created envs resides in one place and the path is configured by a config. Possible choice of config place are `~/.config/gxenv/config.json` and `/etc/gxenv/config.json`.


Example of config.json
----------------------

Here is an example of config which declares the env path.

```
{
    "env_base": "/var/lib/python3/envs/"
}
```

