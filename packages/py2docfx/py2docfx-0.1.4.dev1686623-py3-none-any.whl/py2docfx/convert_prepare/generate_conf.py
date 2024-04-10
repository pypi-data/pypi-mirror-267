from collections import defaultdict
import json
import os
from datetime import datetime
from sphinx.cmd.quickstart import generate
from py2docfx.convert_prepare.package_info import PackageInfo

defaultExtensions = ["sphinx.ext.autodoc",
                     "sphinx.ext.napoleon",
                     "sphinx.ext.extlinks",
                     "yaml_builder"
                     ]


def generate_conf(package: PackageInfo, output: str, template_dir: str):
    params = defaultdict(str)
    params["quiet"] = True

    # index.rst configuration
    params["master"] = "index"
    params["suffix"] = '.rst'

    # conf.py configuration
    extension_list = defaultExtensions.copy()
    extension_list[-1: -1] = getattr(package, "sphinx_extensions", [])
    params["EXTENSIONS"] = json.dumps(extension_list)

    params["PROJECT_NAME"] = getattr(package, "name", "")
    params["FOLDER"] = getattr(package, "folder", "")
    params["YEAR"] = datetime.now().strftime("%Y")
    params["AUTHOR_NAME"] = getattr(package, "author", "")
    params["PROJECT_VERSION"] = getattr(package,"version", "")
    params["PROJECT_RELEASE"] = getattr(package,"version", "")

    extension_config = []
    if hasattr(package, "extension_config"):
        for key, value in package.extension_config.items():
            extension_config.append(" = ".join([key, json.dumps(value)]))
        params["EXTENSION_CONFIG"] = "\n".join(extension_config)

    # Write the final conf.py file.
    output = output.strip()
    if not output:
        output = "."
    else:
        if output.endswith("conf.py"):
            # Make sure the Output is a folder path.
            output = os.path.dirname(output)

        if not os.path.exists(output):
            # The folder is not there, so that we need to create one.
            os.makedirs(output)

    # Write the conf.py and index.rst file to the output folder.
    params["path"] = output
    generate(params, overwrite=True, silent=True, templatedir=template_dir)

    # remove unused folder auto-generated by sphinx
    for folder in ["build", "static", "templates"]:
        dir_to_remove = os.path.join(output, folder)
        if os.path.exists(dir_to_remove):
            os.removedirs(dir_to_remove)
