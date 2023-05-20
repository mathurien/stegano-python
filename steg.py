from ipython_display import imshow, imread, imsave
import sys
"""imsave(filename, img)"""

def createImg(p: int, n: int) :
    """ Renvoie une image entièrement noire de $p$ lignes et $n$ colonnes.
    """
    grid = [0]*p
    i = 0
    while i < len(grid) :
        grid[i] = [0] * n
        i = i + 1
    i = 0
    j = 0
    while i < p :
        while j < n :
            grid[i][j] = (0,255,255)
            j = j + 1
        j = 0
        i = i + 1
    return grid

def binary(n: int):
    """
    Calcule la représentation binaire d'un entier.

    """
    if n == 0:
        return "00000000"
    binaryStr = ""
    while n > 0:
        binaryStr = str(n % 2) + binaryStr
        n //= 2
        
    for i in range(8 - len(binaryStr)):
        binaryStr = "0" + binaryStr

    return binaryStr

def imgBinary(L):
    """
    Renvoie l'écriture binaire de l'image matricielle RVB L donnée en entrée
    
    """
    
    binaryImg = createImg(len(L), len(L[0]))
    for i in range(len(L)):
        for j in range(len(L[i])):
            binaryImg[i][j] = binary(L[i][j][0]), binary(L[i][j][1]), binary(L[i][j][2])
    return binaryImg

def binToInt(binStr):
    """Convertit une chaîne de caractères binaire en entier."""
    intOut = 0
    for i, bit in enumerate(binStr[::-1]):
        if bit == '1':
            intOut += 2**i
    return intOut

def binToIntImg(imgBin):
    intImg = createImg(len(imgBin), len(imgBin[0]))
    for i in range(len(imgBin)):
        for j in range(len(imgBin[i])):
            intImg[i][j] = binToInt(imgBin[i][j][0]), binToInt(imgBin[i][j][1]), binToInt(imgBin[i][j][2])
    return intImg

def wBit(octet, level):
    newOct = ""
    if octet == "00000000":
        return octet
    for k in range(0, 8 - level):
        newOct += octet[k]
    for i in range(level):
        newOct += "0"
    return newOct

def delWeakBits(imgBin, level):
    imgBinWeak = createImg(len(imgBin), len(imgBin[0]))
    for i in range(len(imgBin)):
        for j in range(len(imgBin[i])):
            imgBinWeak[i][j] = wBit(imgBin[i][j][0], level), wBit(imgBin[i][j][1], level), wBit(imgBin[i][j][2], level),
    return imgBinWeak

def splitBinMsg(binMsg, level):
    if level not in [1, 2, 4]:
        raise ValueError("le niveau de cache doit etre égal a 1, 2 ou 4")
    splitMsgBin = []
    i = 0
    while i < len(binMsg):
        splitMsgBin.append(binMsg[i:i + level])
        i += level
    return splitMsgBin

def generateKey(level):
    if level == 1 :
        return "00"
    if level == 2 :
        return "01"
    if level == 4 :
        return "11"
def getLevel(x, y, msg):
    pixelCount = x*y
    if len(msg)*8 + 15 < pixelCount :
        return 1
    elif len(msg)*4 + 15 < pixelCount :
        return 2
    elif len(msg)*2 + 15 < pixelCount :
        return 4
    else :
        raise ValueError("l'image est trop petite pour y encoder le message")

def hideMsg(msg, img, level):
    """
    msg = str
    img = [][](bin: r, bin: v, bin: b)
    level = number of bytes to delete
    """
    newImg = createImg(len(img), len(img[0]))
    msgList = []
    for letter in msg:
        if ord(letter) > 255:
            nothing = 0
        else:
            msgList.append(ord(letter))
    #^création de msgList
    msgListBin = [""]*(len(msgList))
    for i in range(len(msgList)):
        msgListBin[i] = binary(msgList[i])
    #^convertion de msgList en binaire
    splitMsgListBin = []
    i = 0
    for i in range(len(msgListBin)) :
        for element in splitBinMsg(msgListBin[i], level):
            splitMsgListBin.append(element)
#    print(splitMsgListBin)
    #^séparation de chaque octet en 8/level 
    cpt = 0
    cpt1 = 0
    newImg[0][0] = img[0][0][0], img[0][0][1], img[0][0][2][:6] + generateKey(level)
    for i in range(len(img)):
        for j in range(len(img[i])):
            if i+j != 0 :
                if cpt < len(splitMsgListBin):
                    newImg[i][j] = img[i][j][0], img[i][j][1], img[i][j][2][:8-level] + splitMsgListBin[cpt]
                else :
                    if cpt1 < 15:
                        newImg[i][j] = img[i][j][0], img[i][j][1], img[i][j][2][:8-level] + level*"0"
                        cpt1 += 1
                    else :
                        newImg[i][j] = img[i][j]
                cpt += 1
    return newImg

def findLevel(level) :
    if level == "00":
        return 1
    if level == "01":
        return 2
    if level == "11":
        return 4

def findMsg(img):
    level = findLevel(img[0][0][2][6:])
    splitMsgBin = []
    cpt = 0
    for i in range(len(img)):
        for j in range(len(img[i])):
            if i+j != 0 :
                if cpt < 14:
                    splitMsgBin.append(img[i][j][2][8-level:])
                    if img[i][j][2][8-level:] == "0"*level:
                        cpt += 1
                    else:
                        cpt = 0
                else :
                    break
#    print("splitMsgBin: ",splitMsgBin)
    msgBin = []
    octet = ""
    for part in splitMsgBin:
        if len(octet) < 8:
            octet = octet+part
        else :
            msgBin.append(octet)
            octet = part
#    print("msgBin: ",msgBin)

    if level == 4:
        for i in range(6):
            msgBin.pop(len(msgBin)-1)
    elif level == 2:
        for i in range(3):
            msgBin.pop(len(msgBin)-1)
    elif level == 1:
        msgBin.pop(len(msgBin)-1)
#    print("msgBin: ",msgBin)

    msg = ""
    for element in msgBin:
        msg = msg+chr(binToInt(element))
    return msg

if sys.argv[1] == "-e":
    img = imread(sys.argv[3])
    print("img ", sys.argv[3], " loaded, converting to binary...")
    img = imgBinary(img)
    print("hiding message...")
    
    msg = sys.argv[2]
    img = hideMsg(msg, img, getLevel(len(img), len(img[0]), msg))
    print("level: ", getLevel(len(img), len(img[0]), msg))
    
    img = binToIntImg(img)
    imsave("encoded-img.png", img)
    print("image saved as encoded-img.png")
elif sys.argv[1] == "-d":
    img = imread(sys.argv[2])
    img = imgBinary(img)
    msg = findMsg(img)
    print(msg)
elif sys.argv[1] == "-ef":
    img = imread(sys.argv[3])
    print("img ", sys.argv[3], " loaded, converting to binary...")
    img = imgBinary(img)
    print("hiding message...")
    with open(sys.argv[2], "r") as file:
        msg = file.read()

    img = hideMsg(msg, img, getLevel(len(img), len(img[0]), msg))
    print("level: ", getLevel(len(img), len(img[0]), msg))
    
    img = binToIntImg(img)
    imsave("encoded-img.png", img)
    print("image saved as encoded-img.png")
elif sys.argv[1] == "-df":
    img = imread(sys.argv[2])
    img = imgBinary(img)
    msg = findMsg(img)
    with open("found-msg.txt", "w") as file:
        file.write(msg)

