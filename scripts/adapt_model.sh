show_help() {
  echo "usage: $0 <original-model> <audio-data-dir> <dict>"
}

# Args
ORIGINAL_MODEL=$1
AUDIO_DATA=$2
ORIGINAL_DICT=$3

# Validate Args
if [[ -z "$ORIGINAL_MODEL" ]] || [[ -z "$AUDIO_DATA" ]] || [[ -z "$ORIGINAL_DICT" ]]
then
  show_help
  exit -1
fi

# Constants
ORIGINAL_MODEL_NAME=original-model
SPHINX_TRAIN_HOME=/usr/local/libexec/sphinxtrain


cp -R $ORIGINAL_MODEL $AUDIO_DATA/$ORIGINAL_MODEL_NAME
cp $ORIGINAL_DICT $AUDIO_DATA/lang.dict

pushd $AUDIO_DATA



FILE_IDS=$(ls *.fileids)
TRANSCRIPTION=$(ls *.transcription)
DICT=$(ls *.dict)

sphinx_fe -argfile $ORIGINAL_MODEL_NAME/feat.params \
    -samprate 16000 -c $FILE_IDS \
    -di . -do . -ei wav -eo mfc -mswav yes

pocketsphinx_mdef_convert -text $ORIGINAL_MODEL_NAME/mdef $ORIGINAL_MODEL_NAME/mdef.txt

cat $ORIGINAL_MODEL_NAME/feat.params > bw.params
sed -i '/-lowerf/d' bw.params
sed -i '/-upper/d' bw.params
sed -i '/-nfilt/d' bw.params
sed -i '/-transform/d' bw.params
sed -i '/-lifter/d' bw.params
sed -i '/-model/d' bw.params

ORIGINAL_FEAT_PARAMS=$(tr '\n' ' ' < bw.params)

$SPHINX_TRAIN_HOME/bw $ORIGINAL_FEAT_PARAMS \
    -ts2cbfn .ptm. \
    -hmmdir $ORIGINAL_MODEL_NAME \
    -moddeffn $ORIGINAL_MODEL_NAME/mdef.txt \
    -ctlfn $FILE_IDS \
    -lsnfn $TRANSCRIPTION \
    -dictfn $DICT \
    -accumdir .

$SPHINX_TRAIN_HOME/mllr_solve \
    -meanfn $ORIGINAL_MODEL_NAME/means \
    -varfn $ORIGINAL_MODEL_NAME/variances \
    -outmllrfn mllr_matrix -accumdir .

cp -a $ORIGINAL_MODEL_NAME $ORIGINAL_MODEL_NAME-adapt

$SPHINX_TRAIN_HOME/map_adapt \
    -moddeffn $ORIGINAL_MODEL_NAME/mdef.txt \
    -ts2cbfn .ptm. \
    -meanfn $ORIGINAL_MODEL_NAME/means \
    -varfn $ORIGINAL_MODEL_NAME/variances \
    -mixwfn $ORIGINAL_MODEL_NAME/mixture_weights \
    -tmatfn $ORIGINAL_MODEL_NAME/transition_matrices \
    -accumdir . \
    -mapmeanfn $ORIGINAL_MODEL_NAME-adapt/means \
    -mapvarfn $ORIGINAL_MODEL_NAME-adapt/variances \
    -mapmixwfn $ORIGINAL_MODEL_NAME-adapt/mixture_weights \
    -maptmatfn $ORIGINAL_MODEL_NAME-adapt/transition_matrices

$SPHINX_TRAIN_HOME/mk_s2sendump \
    -pocketsphinx yes \
    -moddeffn $ORIGINAL_MODEL_NAME-adapt/mdef.txt \
    -mixwfn $ORIGINAL_MODEL_NAME-adapt/mixture_weights \
    -sendumpfn $ORIGINAL_MODEL_NAME-adapt/sendump

popd