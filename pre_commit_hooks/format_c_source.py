"""
This module runs various style tools to format source code files.  It is meant to be used
in conjunction with the python module precommit (https://pre-commit.com/) to help enforce
guidelines before code is committed to a git repository.
"""
import os
import subprocess
import argparse
import shutil
import sys
from typing import (
    Optional,
    Sequence
)

def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    Format specified text source files

    :param argv: list of filenames to process
    :return program exit code, 0 = success, > 0 fail (1 for generic error)
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
        )

    # Eventually we can add other tool options here...
    parser.add_argument(
        '-a', '--astyle', type=str,
        help='path to astyle config file',
        )
    parser.add_argument(
        '-c', '--clangformat', type=str,
        help='path to clang-format options file',
        )

    args = parser.parse_args(argv)

    if not (args.astyle or args.clangformat):
        parser.error('No action requested, add --astyle or --clangformat')

    # Bail early if there are no files to process
    if len(args.filenames) == 0:
        print('No files')
        return 0

    # Note: sourcetree doesn't use the same system path when running commit hooks (there
    # is a bug in their tool).  We can try to fix that here (not really sure what
    # happens on windows -- so not handling that now)
    if sys.platform != 'win32':
        if '/usr/local/bin' not in os.environ['PATH']:
            os.environ['PATH'] += os.pathsep + '/usr/local/bin'

    if args.astyle:
        # check to make sure astyle is installed
        locate = shutil.which('astyle')

        if locate is None:
            print('astyle executable not found on in PATH, is it installed?')
            print('Consult your favorite package manager for installation')
            print('(e.g. \'brew install astyle\' on mac or \'apt-get install astyle\' on Ubuntu)')
            return 1

        # Check to make sure that options file is present
        if not os.path.exists(args.astyle):
            print(f'{args.astyle} not found. Please check that the file exists')
            return 1

        # Run astyle
        for fname in args.filenames:
            # Since check=True below, this will throw an exception if the call
            # to astyle fails for some reason.  Note, as long as the options and
            # filename passed to astyle are OK, it should never fail (always returns
            # a '0' whether it formatted a file or not.  Need to check the output
            # to know if it actually changed anything in the file or not.
            astyle_result = subprocess.run(["astyle",
                                "--options=" + args.astyle, fname],
                                capture_output=True, text=True,
                                check=True)

            if 'Formatted' in astyle_result.stdout:
                print('Formatted: ' + fname)
        

    if args.clangformat:
        # check to make sure astyle is installed
        locate = shutil.which('clang-format')

        if locate is None:
            print('clang-format executable not found on in PATH, is it installed?')
            print('Consult your favorite package manager for installation')
            print('(e.g. \'brew install clang-format\' on mac or \'apt-get install clang-format\' on Debian/Ubuntu)')
            return 1

        # Check to make sure that options file is present
        if not os.path.exists(args.clangformat):
            print(f'{args.clangformat} not found. Please check that the file exists')
            return 1

        # Run clang-format
        for fname in args.filenames:
            # Since check=True below, this will throw an exception if the call
            # to clang-format fails for some reason.  Note, as long as the options and
            # filename passed to clang-format are OK, it should never fail.

            # First do a dry run to see if the file needs formatting or not
            # (this is just to support better info being printed during execution)
            clang_result = subprocess.run(["clang-format",
                                           "--dry-run",
                                           "--Werror",
                                           "--style=file:" + args.clangformat,
                                           "-i", fname],
                                           capture_output=True, text=True)

            if clang_result.returncode != 0:
                # Error code set means the file needs formatting
                clang_result = subprocess.run(["clang-format",
                                           "--style=file:" + args.clangformat,
                                           "-i", fname])

                if clang_result.returncode == 0:
                    print('Formatted: ' + fname)
                else:
                    print('clang-format can not format file: ' + clang_result.stdout)
                    return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
