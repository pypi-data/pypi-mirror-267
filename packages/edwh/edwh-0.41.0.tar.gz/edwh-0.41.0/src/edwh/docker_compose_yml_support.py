import yaml, os, re
from pathlib import Path

envvar_matcher = re.compile(r"\$\{([^}^{]+)\}")


def envvar_constructor(loader, node):
    """Extract the matched value, expand env variable, and replace the match"""
    value = node.value
    match = envvar_matcher.match(value)
    env_var = match.group()[2:-1]
    if "?" in env_var:
        env_var, default = env_var.split("?")

    return os.environ.get(env_var) + value[match.end() :]


yaml.add_implicit_resolver("!envvar", envvar_matcher)
yaml.add_constructor("!envvar", envvar_constructor)


def load_compose_str(str):
    return yaml.load(str, Loader=yaml.FullLoader)


def load_compose_file(path: Path):
    with path.open("r") as f:
        return load_compose_str(f.read())


_test = """ 
simple: ${PATH}
default: ${PATH:default}
"""
if __name__ == "__main__":
    import sys

    print(load_compose_str(test))
