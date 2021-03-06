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
        Get all the imports
        """
        for alias in node.names:
            # print(alias.__dict__)
            self.stats.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """
        Get all the 'from' imports
        """
        for alias in node.names:
            # print(node.module)
            self.stats.append(node.module)
        self.generic_visit(node)

    def report(self):
        """
        Convert the output to a list
        """
        return list(set(self.stats))


def get_imports(tree):
    """
    Walk the given ast to extract all the imports used.
    :param tree: abstrax synta tree of a file
    :return: list of all imports used in the tree
    """
    source_walker = WALKER()
    source_walker.visit(tree)
    return source_walker.report()


def process_file(filename):
    """
    Parse given python file and get the parsed ast.
    :param filename: name of the python file to be read
    :return: parsed abstract syntax tree
    """
    # Not checking existance of file because it was already checked previously.
    parsed_source = None
    with open(filename, 'rb') as py_file:
        parsed_source = ast.parse(py_file.read())
    return parsed_source


def process_dir(dir_path):
    """
    Iterate through directories and sub-directories and capture all python files
    :param dir_path: root path
    :return: list of file paths of .py files
    """
    # Read all files that have the extension .py
    py_files = []
    for (dirpath, dirnames, filenames) in os.walk(dir_path):
        for file in filenames:
            if file.endswith('.py'):
                file_path = "{0}\{1}".format(dirpath, file)
                py_files.append(file_path)
    return py_files

def remove_stopwords(imports):
    my_stopwords = ["app","config","tests"]
    clean_imports = [l.split('.')[0] for l in imports]
    #clean_imports = [l.split('_')[0] for l in clean_imports]
    clean_imports = [l for l in clean_imports if l not in my_stopwords]

    return clean_imports

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
    user_dir_imports = []
    used_file_imports=[]
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
            if py_files:
                #print(py_files)
                for py_file in py_files:
                    #print(py_file)
                    try:
                        sourced_file = process_file(py_file)
                        used_file_imports = get_imports(sourced_file)
                        user_dir_imports = user_dir_imports + used_file_imports
                    except SyntaxError:
                        print("There was a problem reading: ",py_file)
                #print(list(set(user_dir_imports)))
            else:
                print("No .py files found!")

        else:
            print("Invalid directory name or  directory does not exist.")
    else:
        print("No File/Directory specified! Please type the fullpath.")
    all_imports = list(set(user_dir_imports))
    #Some clean up before presenting the imports
    all_imports = remove_stopwords(all_imports)
    imports = "The following imports were used:\n {0}. \n You could use pip3 install -U [module_name] to install the " \
              "dependencies.".format(", ".join(list(set(all_imports))))
    print(imports)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
