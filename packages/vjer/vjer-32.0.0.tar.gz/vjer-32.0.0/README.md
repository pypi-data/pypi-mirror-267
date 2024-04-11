# Vjer Python Module

A module for automating CI/CD tasks.

## Developing

Development is best accomplished using virtualenv or virtualenv-wrapper where a virtual environment can be generated:

    mkvirtualenv vjer
    python -m pip install --upgrade pip
    pip install --upgrade --upgrade-strategy eager setuptools wheel
    pip install --upgrade --upgrade-strategy eager flit
    Windows: flit install --deps all
    Linux: flit install -s --deps all

To update the current development environment

    python -m pip install --upgrade pip
    pip install --upgrade --upgrade-strategy eager setuptools wheel
    Windows: pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
    Linux: pip freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install --upgrade

## Testing

### Static Analysis

The static analysis test can be run with

    pylint vjer
    flake8 vjer
    mypy vjer

### Unit Tests

The unit tests can be run with

    python -m unittest -v [tests.test_suite[.test_class[.test_case]]]

## Building

The build can be run with

    flit build

## Publishing a Release

This is the procedure for releasing Vjer

1. Validate all issues are "Ready for Release"
1. Update CHANGELOG.md
1. Run the release workflow against the Production environment
1. Validate GitHub release
1. Validate PyPi
1. Move issues to "Closed" and label res::complete
1. Close Milestone
1. Update source in Perforce

<!--- cSpell:ignore virtualenv mkvirtualenv vjer stest mypy xmlrunner utest -->
