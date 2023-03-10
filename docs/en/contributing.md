# Contributing
KMK is a community effort and welcomes contributions of code and documentation from people 
of all backgrounds and levels of technical skill. As such, these guidelines should serve 
to make contributing as easy as possible for everyone while maintaining a consistent style.

## Contributing Code
The following guidelines should ensure that any code contributed can be merged in as 
painlessly as possible. If you're unsure how to set up your development environment, 
feel free to [join our Zulip community](https://kmkfw.zulipchat.com).

### Code Style

KMK uses [Black](https://github.com/psf/black) with a Python 3.6 target and,
[(controversially?)](https://github.com/psf/black/issues/594) single quotes.
Further code styling is enforced with isort and flake8 with several plugins.

**NOTE:** before committing code, run `make fix-isort fix-formatting test` to 
reduce workload for the project's maintainers and prevent the CI pipeline from 
failing.

There are some limited exceptions to the code formatting rules, which can be 
found in `setup.cfg`, notably around `user_keymaps` (which are also not subject 
to Black formatting as documented in `pyproject.toml`)

### Tests

Unit tests within the `tests` folder mock various CircuitPython modules to allow
them to be executed in a desktop development environment.

Execute tests using the command `make unit-tests`. The unit-tests target accepts
an optional environment variable for specifying a subset of tests with python
unittest syntax:
```sh
make unit-tests TESTS="tests.test_capsword tests.test_hold_tap"
```

## Contributing Documentation
While KMK welcomes documentation from anyone with and understanding of the issues 
and a willingness to write them up, it's a good idea to familiarize yourself with 
the docs. Documentation should be informative but concise.

### Styling
Docs are written and rendered in GitHub Markdown.
Check out this comprehensive [guide to basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) from GitHub's documentation.

In particular, KMK's docs should include a title, demarcated with `#`, and subheadings 
should be demarcated with `##`, `###`, and so on. Headings should be short and specific.

### Example Code
Where possible, practical code examples should be included in documentation to help 
new users understand how to implement features. In general, it's better to have a code-
block with comments inside it rather than multiple blocks of code broken up with 
explanation.

Code blocks should be formatted as Python code as follows:
````
```python
print('Hello, world!')
```
````

Inline code, indicated with `` `backticks` ``, should be used when calling out specific 
functions or Python keywords within the body of paragraphs or in lists.

## License, Copyright, and Legal

All software in this repository is licensed under the [GNU Public License,
version 3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)).
All documentation and hardware designs are licensed under the [Creative Commons
Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
license. Contributions to this repository must use these licenses unless
otherwise agreed to by the Core team.
