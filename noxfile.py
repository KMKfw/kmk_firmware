import nox
import shutil
from pathlib import Path

source_dir = Path('kmk')
build_dir = Path('build')


@nox.session
def black(session):
    '''Format python code with `black`.'''
    session.install('black')
    session.run('black', source_dir)


@nox.session
def isort(session):
    session.install('isort')
    session.run('isort', source_dir)


@nox.session
def flake8(session):
    session.install('flake8')
    session.run('flake8', source_dir)


@nox.session
def clean(session):
    build_dir.mkdir(exist_ok=True)
    for child in build_dir.iterdir():
        if child.is_file():
            child.unlink()
        else:
            shutil.rmtree(child)


@nox.session
def compile(session):

    clean(session)

    shutil.copy2('boot.py', 'build/boot.py')

    # Make sure the full folder heirarchy exists
    for d in source_dir.glob('**/'):
        if not build_dir.joinpath(d).exists():
            Path.mkdir(build_dir.joinpath(d))

    # Compile every python file
    for x in source_dir.glob('**/*.py'):
        out_path = str(build_dir.joinpath(x).with_suffix('.mpy'))
        session.run('mpy-cross', f'{x}', '-o', f'{out_path}', external=True)


nox.options.sessions = ['black', 'isort']  # Default sessions
