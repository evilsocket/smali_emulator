"""Exec Smali Files.

Usage:
    exec.py -i File.smali -m methodName [-p methodParameters]

Options:
    -h --help        Show this screen.
    -i <filename>    The smali file to execute.
    -m <method>      The name of the method to execute.
    -p <parameters>  A list of parameters to give as arguments.
                     If not provided, the script will introspect the method
                     and give insights about what parameters are expected.
"""

from docopt import docopt
import smali.emulator

def main(arguments):
    filename = arguments.get('-i')
    method = arguments.get('-m')
    parameters = arguments.get('-p')
    vm = smali.emulator.Emulator()

    if parameters:
        result = vm.run(filename, method, parameters)
    else:
        result = vm.inspect(filename, method)

    print(results)

if __name__ == '__main__':
    main(docopt(__doc__))
