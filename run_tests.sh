#!/bin/bash
# run_tests.sh
set -eu

# Shell options

NONE='\033[00m'
RED='\033[01;31m'
GREEN='\033[01;32m'
YELLOW='\033[01;33m'
PURPLE='\033[01;35m'
CYAN='\033[01;36m'
WHITE='\033[01;37m'
BOLD='\033[1m'
UNDERLINE='\033[4m'

PREFIX="$BOLD>>> run_test.sh >>>$NONE"

function usage {
  echo "Usage: $0 [OPTION]..."
  echo "Run viaplay test suite"
  echo ""
  echo "  -i, --integration        Run the integration test end-to-end"
  echo "  -x, --stop               Stop running test after the first error or failure"
  echo "  -p, --pep8               Just run flake8"
  echo "  -P, --no-pep8            Don't run flake8"
  echo "  -c, --coverage           Generate coverage report"
  echo "  -h, --help               Print this usage message"
  echo ""
  echo "Note: with no options specified, the script will try to:"
  echo -e "\t - Run the unittest functional tests"

  exit
}

function process_option {
  case "$1" in
    -h|--help) usage;;
    -f|--force) force=1;;
    -i|--integration) integration=1;;
    -u|--update) update=1;;
    -p|--pep8) just_flake8=1;;
    -P|--no-pep8) no_flake8=1;;
    -c|--coverage) coverage=1;;
    -x|--stop) stop=1;;
    -*) testopts="$testopts $1";;
    *) testargs="$testargs $1"
  esac
}

integration=0
stop=0
testargs=
testopts="--with-xunit"
wrapper=""
just_flake8=0
no_flake8=0
coverage=0
debug=0
update=0

LANG=en_US.UTF-8
LANGUAGE=en_US:en
LC_ALL=C
OS_STDOUT_NOCAPTURE=False
OS_STDERR_NOCAPTURE=False

for arg in "$@"; do
  process_option $arg
done

#Configuration of the test framework
NOSE="nosetests"
TESTRTESTS=$NOSE

function run_tests {
  # Cleanup *.pyc
  ${wrapper} find . -type f -name "*.pyc" -delete

  # Start the fake server
  python ./viaplay/tests/fake_movie_info.py &
  pid_save=$!

  if [ "$testopts" = "" ]; then
    testopts="-v"
  fi

  if [ $stop -eq 1 ]; then
    testopts="$testopts -x"
  fi

  if [ "$testargs" = "" ]; then
    testargs=""
  fi

  if [ $coverage -eq 1 ]; then
     testopts="$testopts --with-coverage --cover-erase --cover-package=viaplay "
  fi

  if [ $integration -eq 0 ]; then
    testopts="$testopts -a '!integration'"
  fi

  # Just run the test suites in current environment
  set +e
  testargs=`echo "$testargs" | sed -e's/^\s*\(.*\)\s*$/\1/'`
  TESTRTESTS="$TESTRTESTS $testargs $testopts"
  echo -e "$PREFIX Running \`${wrapper} $TESTRTESTS\`"
  bash -c "${wrapper} $TESTRTESTS"
  RESULT=$?
  set -e

  kill $pid_save

  return $RESULT
}

function run_flake8 {
  echo -e "$PREFIX Running pep8 ..."
  pep8 --max-line-length=120 viaplay >pep8.log || true
  echo -e "$PREFIX Running pyflakes ..."
  pyflakes viaplay >pyflakes.log || true
  # Just run Flake8 in current environment
  # ${wrapper} flake8 ${srcfiles}
}


if [ $just_flake8 -eq 1 ]; then
    run_flake8
    exit
fi

run_tests

if [ $no_flake8 -eq 0 ]; then
    run_flake8
    exit
fi
