#!/bin/csh -f
setenv LIA_TAGG /usr/local/lia_tagg
setenv LIA_TAGG_LANG french
cd $LIA_TAGG
make clean
make all
make ressource.french

#echo "je veux peut être neTTOyée ma pomme de terre" | $LIA_TAGG/script/lia_clean