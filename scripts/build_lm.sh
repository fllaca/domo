set -e

show_help() {
  echo "usage: $0 <sentences-file> <lm-name>"
}

SENTENCES=$1
LM_NAME=$2

# Validate Args
if [[ -z "$SENTENCES" ]] || [[ -z "$LM_NAME" ]]
then
  show_help
  exit -1
fi

SRILM_HOME=/usr/share/srilm/bin/i686-m64

# -kndiscount -interpolate
$SRILM_HOME/ngram-count -text $SENTENCES -lm $LM_NAME.lm -debug 1

$SRILM_HOME/ngram -lm $LM_NAME.lm -prune 1e-8 -write-lm $LM_NAME-pruned.lm

#After training it is worth it to test the perplexity of the model on the test data:
#ngram -lm your.lm -ppl test-text.txt

