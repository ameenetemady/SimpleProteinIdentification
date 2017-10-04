#!/bin/bash

echo -n 18mix: ; python3.5 getAUC.py ref/18mix_reference.csv data/18mix/pred.csv
echo -n UPS2: ; python3.5 getAUC.py ref/UPS_reference.csv data/UPS2/pred.csv
echo -n Sigma49: ; python3.5 getAUC.py ref/Sigma_49_reference.csv data/Sigma49/pred.csv
echo -n yeast: ; python3.5 getAUC.py ref/yeast_ref5.csv data/Yeast/pred.csv
echo -n HumanEKC: ;  python3.5 getAUC.py ref/HumanEKC_reference.csv data/HumanEKC/pred.csv 
echo -n HumanMD: ; python3.5 getAUC.py ref/HumanMD_reference.csv data/HumanMD/pred.csv 
echo -n DME: ; python3.5 getAUC.py ref/DME_reference.csv data/DME/pred.csv 

