mkdir -p /usr/share/srilm
cp srilm-1.7.2.tar.gz /usr/share/srilm/
cd /usr/share/srilm
tar xvf srilm-1.7.2.tar.gz

# tcsh
# make NO_TCL=1 MACHINE_TYPE=x86_64-gcc4 World
# ./bin/i686-gcc4/ngram-count -help