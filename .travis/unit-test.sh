#!/bin/bash

set -e
errors=0

# Run unit tests
python insighter/insighter_test.py || {
    echo "'python python/insighter/insighter_test.py' failed"
    let errors+=1
}

# Check program style
pylint -E insighter/*.py || {
    echo 'pylint -E insighter/*.py failed'
    let errors+=1
}

[ "$errors" -gt 0 ] && {
    echo "There were $errors errors found"
    exit 1
}

echo "Ok : Python specific tests"
