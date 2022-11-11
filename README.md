# fw-precommit-hooks
Contains custom hooks for the [pre-commit](https://pre-commit.com/) python package for checking source code. 

## Support
This works with two different tools to format source code with the help of pre-commit:
 * [astyle](https://astyle.sourceforge.net/) - an old package that does a pretty decent job, but no longer maintained
 * [clang-format](https://clang.llvm.org/docs/ClangFormat.html) - a newer tools that is well supported with lots of formatting options

## Usage
In order to use this, you need to add a section to your .pre-commit-config.yaml file to get this hook that specifies which of the formatters you want to use and give it a path to the options file(s).  You can use either or both `astyle` or `clang-format`

Here is an example of clang format usage:
```
-   repo: https://github.com/delsauce/pre-commit-hooks
    rev: v1.0.0
    hooks:
    -   id: format-c-source
        types: [file, c]
        args: [--clangformat, 'path-to-clang-format-options-file']
```

If you'd rather use `astyle` change the args:
```
        args: [--astlye, 'path-to-astyle-options-file']
```
