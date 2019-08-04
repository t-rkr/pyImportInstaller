'''
@author: Tarun
'''

import os
import sys
import ast
import logging
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
LOGGER = logging.getLogger("Main")

class WALKER(ast.NodeVisitor):
    """
    Helper class to walk thorugh nodes of the tree produced by ast.
    """

    def __init__(self):
        self.stats = []

    def visit_Import(self, node):
        """

        :param node:
        :return:
        """
        for alias in node.names:
            # print(alias.__dict__)
            self.stats.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """

        :param node:
        :return:
        """
        for alias in node.names:
            # print(node.module)
            self.stats.append(node.module)
        self.generic_visit(node)

    def report(self):
        """

        :return:
        """
        return list(set(self.stats))


def get_imports(tree):
    """

    :param tree:
    :return:
    """
    source_walker = WALKER()
    source_walker.visit(tree)
    return source_walker.report()


def process_file(filename):
    """

    :param filename:
    :return:
    """
    # Not checking existance of file because it was already checked previously.
    parsed_source = None
    with open(filename, 'rb') as py_file:
        parsed_source = ast.parse(py_file.read())
    return parsed_source


def process_dir(dir_path):
    """

    :param dir_path:
    :return:
    """
    # Read all files that have the extension .py
    py_files = []
    for (dirpath, dirnames, filenames) in os.walk(dir_path):

        for file in filenames:
            if file.endswith('.py'):
                file_path = "{0}\{1}".format(dirpath, file)
                py_files.append(file_path)
    return py_files


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--file', '-f', help="File to read for imports")
@click.option('--dir', '-d', help="Root of the directory containing .py files")
def main(file, dir):
    """
    Display all the imports specified in a particular .py file or
    in a python project containing multiple .py files
    """
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug("Debugger")
    if file:
        if os.path.isfile(file):
            sourced_file = process_file(file)
            used_file_imports = get_imports(sourced_file)
            print(used_file_imports)

        else:
            print("Invalid filename or  File does not exist.")
    elif dir:
        if os.path.isdir(dir):
            py_files = process_dir(dir)
            user_dir_imports = []
            if py_files:
                print(py_files)
                for py_file in py_files:
                    print(py_file)
                    try:
                        sourced_file = process_file(py_file)
                        used_file_imports = get_imports(sourced_file)
                        user_dir_imports = user_dir_imports + used_file_imports
                    except SyntaxError:
                        print("There was a problem reading: ",py_file)
                print(list(set(user_dir_imports)))
            else:
                print("No .py files found!")

        else:
            print("Invalid directory name or  directory does not exist.")
    else:
        print("No File/Directory specified! Please ")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
