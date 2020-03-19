#!/usr/bin/env sh
# Utility to build/upload pip packages
#

CLEAN=
VERSION=
BUILD=
INSTALL=
UPLOAD=

usage() {
    echo "\nUsage:\n"
    echo "   $0 [-c] [-i] [-b] [-u]\n"
    echo "\nPlease use one or more of these options:"
    echo "    -c,  --clean      Clean previous build"
    echo "    -b,  --build      Build the package"
    echo "    -i,  --install    Locally install the package"
    echo "    -u,  --upload     Upload the package to PyPI"
    echo "    -p,  --python     Python command to use with"
    echo "\n    -h,  --help       Shows this message"
    echo
}

if [ -f './Pipfile' ]; then
    CMD='pipenv run python'
else
    CMD='python'
fi

while [ $# -gt 0 ]; do
    key="$1"
    case $key in
        -b|--build)
            BUILD=1
            shift
            ;;
        -i|--install)
            INSTALL=1
            shift
            ;;
        -v|--version)
            VERSION="$2"
            shift
            shift
            ;;
        -u|--upload)
            UPLOAD=1
            shift
            ;;
        -c|--clean)
            CLEAN=1
            shift
            ;;
        -p|--python)
            CMD="$2"
            shift
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option $key"
            usage
            # pipenv run python setup.py --help-commands
            exit 1
            ;;
    esac
done

if [ ! -z "$CLEAN" ]; then
    echo "Cleaning..."
    $CMD setup.py clean
    rm -rf *.egg-info build dist
fi

if [ ! -z "$VERSION" ]; then
    sed -i "s/__version__\s*=\s*'[0-9]\+\.[0-9]\+'/__version__ = '$VERSION'/" appfw/__init__.py
fi

if [ ! -z "$BUILD" ]; then
    echo "Building..."
    $CMD setup.py sdist bdist_wheel
fi

if [ ! -z "$UPLOAD" ]; then
    echo "Uploading..."
    $CMD -m twine upload dist/*
fi

if [ ! -z "$INSTALL" ]; then
    # local install
    # python -m pip install dist/appfw-0.1-py3-none-any.whl
    # pip install .
    pip install -e .
fi

if [ -z "$CLEAN$BUILD$UPLOAD$INSTALL" ]; then
    usage
    exit 1
fi
