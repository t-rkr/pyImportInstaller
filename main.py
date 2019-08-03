'''
@author: Tarun
'''

import click
import os, sys, ast

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class WALKER(ast.NodeVisitor):
    def __init__(self):
        self.stats = []

    def visit_Import(self,node):
        for alias in node.names:
            #print(alias.__dict__)
            self.stats.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self,node):
        for alias in node.names:
            #print(node.module)
            self.stats.append(node.module)
        self.generic_visit(node)

    def report(self):
        return list(set(self.stats))

def get_imports(tree):
    source_walker = WALKER()
    source_walker.visit(tree)
    return source_walker.report()

def process_file(filename):
    #Not checking existance of file because it was already checked previously.
    parsed_source = None
    with open(filename,'rb') as py_file:
        parsed_source = ast.parse(py_file.read())
    return parsed_source

def process_dir(dir_path):
    #Read all files that have the extension .py
    pass

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--file', '-f', help="File to read for imports")
@click.option('--dir', '-d', help="Root of the directory containing .py files")
def main(file, dir):
    """
    Display all the imports specified in a particular .py file or in a python project containing multiple .py files
    """
    if file:
        if os.path.isfile(file):
            sourced_file = process_file(file)
            used_imports = get_imports(sourced_file)
            print(used_imports)

        else:
            print("Invalid filename or  File does not exist.")
    elif dir:
        if os.path.isdir(dir):
            print("Processing...")
        else:
            print("Invalid directory name or  directory does not exist.")
    else:
        print("No File/Directory specified! Please ")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
