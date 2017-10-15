
show_help() {
  echo "usage: $0 <session-name> <sentences-file>"
}

SESSION=$1
SENTENCES=$2

if [[ -z "$SESSION" ]] || [[ -z "$SENTENCES" ]]
then
  show_help
  exit -1
fi

COUNTER=0
SESSION_ID=$(date "+%Y%m%d-%H%M%S")

mkdir -p $SESSION

# >$SESSION/$SESSION.transcription
# >$SESSION/$SESSION.fileids

while read sentence; do
  FILENAME="${SESSION}_audio_${SESSION_ID}_${COUNTER}"
  echo "Please, press ENTER and read:"
  echo "-----------------------------"
  echo "$sentence"
  read -u 3
  echo "recording..."
  trap ' ' INT
  arecord -c 1 -r 16000 > $SESSION/$FILENAME.wav
  echo "<s>$sentence</s> ($FILENAME)" >>  $SESSION/$SESSION.transcription
  echo "$FILENAME" >>  $SESSION/$SESSION.fileids
  COUNTER=$((COUNTER + 1))
done 3<&0 <$SENTENCES