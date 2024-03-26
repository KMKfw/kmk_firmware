import shutil
import subprocess
from os import devnull, system
from pathlib import Path

source_dir = Path('kmk')
build_dir = Path('build')


def clean():
    build_dir.mkdir(exist_ok=True)
    for child in build_dir.iterdir():
        if child.is_file():
            child.unlink()
        else:
            shutil.rmtree(child)


def compile():

    shutil.copy2('boot.py', 'build/boot.py')

    # Make sure the full folder heirarchy exists
    for d in source_dir.glob('**/'):
        if not build_dir.joinpath(d).exists():
            Path.mkdir(build_dir.joinpath(d))

    # Compile every python file
    for x in source_dir.glob('**/*.py'):
        out_path = str(build_dir.joinpath(x).with_suffix('.mpy'))
        system(f'mpy-cross {x} -o {out_path}')


if __name__ == '__main__':
    try:
        subprocess.run('mpy-cross', stdout=devnull, stderr=devnull)
    except FileNotFoundError:
        print()
        print('`mpy-cross` not found. Ensure mpy-cross is working from a shell.')
        print()
    clean()
    compile()
