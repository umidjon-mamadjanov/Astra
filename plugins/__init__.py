import importlib
import os

def load_plugins():

    plugins = {}

    for file in os.listdir("plugins"):

        if file.endswith(".py") and file != "__init__.py":

            name = file[:-3]

            plugins[name] = importlib.import_module(
                f"plugins.{name}"
            )

    return plugins