# Sphinx tests

## Run

```shell
pocketsphinx_continuous -hmm house_model/original-model-adapt  -lm ../spanish/es-20k.lm -dict ../spanish/es.dict -samprate 16000/8000/48000 -inmic yes -keyphrase "hola"
```

```shell
pocketsphinx_continuous -hmm house_model/original-model-adapt  -dict ./spanish/es.dict -samprate 16000/8000/48000 -inmic yes -agc noise -jsgf commands.gram
```

```shell
./build_lm.sh sentences.txt house
 pocketsphinx_continuous -hmm house_model/original-model-adapt  -lm house-pruned.lm -dict ./spanish/es.dict -samprate 16000/8000/48000 -inmic yes -keyphrase "hola"
 
 # Record samples
 ./record_data.sh house_model sentences.txt
 
 # Adapt Acoustic Model
 ./scripts/adapt_model.sh spanish/cmusphinx-es-5.2/model_parameters/voxforge_es_sphinx.cd_ptm_4000/ house_model spanish/es.dict

 pocketsphinx_continuous -hmm house_model/original-model-adapt  -lm ./spanish/es-20k.lm -dict ./spanish/es.dict -samprate 16000/8000/48000 -inmic yes
```

## Dependencies

Install pico2wave:
```
$ sudo apt-get install libttspico-utils
$ pico2wave -w abc.wav "Good morning. How are you today?"
$ aplay -D plughw:0,0 abc.wav
```

## Refs
* models: https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/Spanish/
* example java: https://www.tinkerfu.com/index.php/posts/keyword-detection-with-pocketsphinx-in-java-part-2
* example rapsberry: https://wolfpaulus.com/embedded/raspberrypi2-sr/
* mic errors: https://github.com/jasperproject/jasper-client/issues/62



