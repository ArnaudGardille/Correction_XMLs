# Correct XML files of PDFs in Factur-X format 

This repository makes use python. 
We recommand you to use the Anaconda distribution.

We run the files through the terminal.
First place youtself if the right folder:
```
cd .../Correction_XMLs 
```
(optional) Create a virtual environment  
```
conda create -n Correction_XMLs
```

```
conda activate Correction_XMLs 
```


Start by installing the requirements:
```
conda install pathlib
pip3 install factur-x
```
Then install your pdf inside the folder 'anciens_fichiers_pdf'.
You can create it if it does not already exist.
Then run:

```
python3 CorrecFatcureX.py
```
And get your corrected files in 'nouveaux_fichiers_pdf' 

Enjoy!

Explanation video (in french)
https://youtu.be/PD4aVITMaIA

nb: If any of thoses command does't work, replace 'pip3' by 'pip' and 'python3' by 'python'.
