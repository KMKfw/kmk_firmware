#!/bin/sh

if ! command -v aspell; then
  echo 'aspell command not found, cannot run spell check'
  exit 1
fi

ROOT=$(git rev-parse --show-toplevel)

# This gets us only english .md files at the moment, but is clearly brittle
MARKDOWN_FILES=$(find "$ROOT" -name '*.md' -not -path '**/.*/**')
# Use our local dict for saved words, and use en_US for the main dict
ASPELL="aspell -M --dont-save-repl -p $ROOT/util/aspell.en.pws -d en_US"

EXIT_STATUS=0
INTERACTIVE=true

# parse flags
if [ -n "$1" ]; then
  if [ "$1" = '--no-interactive' ]; then
    INTERACTIVE=false
  else
    echo "Usage: $0 [--no-interactive]"
    exit 2
  fi
fi

# interactive spell check and correct
if $INTERACTIVE; then
  # run aspell interactively on each file
  for file in $MARKDOWN_FILES; do
    # echo "$ASPELL --dont-backup -c $file"
    $ASPELL --dont-backup -c "$file"
  done
fi

# non-interactive error report
for file in $MARKDOWN_FILES; do
  # echo "cat $file | $ASPELL list"
  BAD_WORDS=$($ASPELL list < "$file" | sort | uniq | tr '\n' '|')
  if [ -n "$BAD_WORDS" ]; then
    EXIT_STATUS=1
    echo \
"'$file' has spelling errors:
$(grep -Eno "$BAD_WORDS" "$file")
To correct spelling on only this file, run the command:
$ASPELL --dont-backup -c $file
"
  fi
done

exit $EXIT_STATUS
