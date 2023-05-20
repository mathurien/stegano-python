# stegano-python
comment utiliser :
il existe 4 paramètres : \n
  -e  (encode, génère l'image "encoded-image.png")
  -d  (decode, affiche le texte)
  -ef  (encode from file, génère l'image "encode-image.png")
  -df  (decode to file, génère le fichier "found-message.txt")
ils s'utilisent comme ça dans un terminal :
python steg.py -e {message} {chemin/vers/image.png}
python steg.py -d {chemin/vers/image/png}
python steg.py -ef {chemin/vers/message.txt} {chemin/vers/image.png}
python steg.py -df {chemin/vers/image.png}
