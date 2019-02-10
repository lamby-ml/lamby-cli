import click
import sys
from tempfile import mkstemp
from shutil import move
import os
from os import fdopen


@click.command('config', short_help='modify configuration parameters')
@click.option('--add', nargs=2, help='usage: --add [key] [value] — adds' +
              ' key/value pair to config file')
@click.option('--change', nargs=2, help='usage: --change [key] [value] ' +
              '— changes key to have given value in config file')
@click.option('--remove', nargs=1, help='usage: --remove [key] ' +
              '— removes the selected key from the config file')
def config(add, change, remove):
    """Modify configuration parameters for this initialized Lamby project"""

    lamby_dir = './.lamby'
    if not os.path.isdir(lamby_dir):  # Check if current dir has .lamby file
        click.echo('Lamby project not initialized in ' + os.getcwd())
        sys.exit(1)

    # add #

    if len(add) != 0:
        # See if key already exists #
        with open(lamby_dir + '/config', "r") as config_file:
            for line in config_file:
                split = line.split(" = ")
                if add[0] == split[0]:
                    click.echo("This key already exists")
                    sys.exit(1)

        config_file = open(lamby_dir + '/config', "a+")
        config_file.write(add[0])
        config_file.write(" = ")
        config_file.write(add[1])
        config_file.write("\n")
        config_file.close()

    # change #

    if len(change) != 0:
        # See if key exists #
        flag = 0
        with open(lamby_dir + '/config', "r") as config_file:
            for line in config_file:
                split = line.split(" = ")
                if change[0] == split[0]:
                    flag = 1
        if flag == 0:
            click.echo("This key does not exist")
            sys.exit(1)
        else:
            fh, abs_path = mkstemp()
            with fdopen(fh, 'w') as temp:
                with open(lamby_dir + '/config', "r") as config_file:
                    for line in config_file:
                        split = line.split(" = ")
                        if change[0] == split[0]:
                            temp.write(change[0])
                            temp.write(" = ")
                            temp.write(change[1])
                            temp.write("\n")
                        else:
                            temp.write(line)
            move(abs_path, lamby_dir + '/config')

    if remove is not None:
        flag = 0
        with open(lamby_dir + '/config', "r") as config_file:
            for line in config_file:
                split = line.split(" = ")
                if remove == split[0]:
                    flag = 1
        if flag == 0:
            click.echo("This key does not exist")
            sys.exit(1)
        else:
            fh, abs_path = mkstemp()
            with fdopen(fh, 'w') as temp:
                with open(lamby_dir + '/config', "r") as config_file:
                    for line in config_file:
                        split = line.split(" = ")
                        if remove != split[0]:
                            temp.write(line)
            move(abs_path, lamby_dir + '/config')
