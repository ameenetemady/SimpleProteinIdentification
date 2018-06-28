#!/bin/bash

python3.5 getAUC.py data/18mix/identification.tsv data/18mix/pred.csv ref/18mix_reference.csv ; echo "(18mix)"
python3.5 getAUC.py data/UPS2/identification.tsv data/UPS2/pred.csv ref/UPS_reference.csv ; echo "(UPS2)"
python3.5 getAUC.py data/Sigma49/identification.tsv data/Sigma49/pred.csv ref/Sigma_49_reference.csv ; echo "(Sigma49)"
python3.5 getAUC.py data/Yeast/identification.tsv data/Yeast/pred.csv ref/yeast_ref5.csv ; echo "(yeast)"
 python3.5 getAUC.py data/HumanEKC/identification.tsv data/HumanEKC/pred.csv DECOY; echo "(HumanEKC)"
python3.5 getAUC.py data/HumanMD/identification.tsv data/HumanMD/pred.csv DECOY; echo "(HumanMD)"
python3.5 getAUC.py data/DME/identification.tsv data/DME/pred.csv DECOY; echo "(DME)"

