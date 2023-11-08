import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller

video = cv2.VideoCapture(1)

video.set(3, 1280)
video.set(4, 720)

kb = Controller()

detector = HandDetector(detectionCon=0.8)
estadoAtual = [0, 0, 0, 0, 0]
ultimoDedoIndicador = 0  # Rastrear o último estado do dedo indicador

setaDir = cv2.imread('seta dir.PNG')
setaEsq = cv2.imread('seta esq.PNG')
setaBai = cv2.imread('seta bai.PNG')  # Imagem para rolar para baixo
setaCim = cv2.imread('seta cim.PNG')  # Imagem para rolar para cima

# Redimensione as imagens para as dimensões desejadas (166x246 pixels)
setaBai = cv2.resize(setaBai, (246, 166))
setaCim = cv2.resize(setaCim, (246, 166))

while True:
    _, img = video.read()
    hands, img = detector.findHands(img)

    if hands:
        estado = detector.fingersUp(hands[0])

        # Rastrear o estado do dedo indicador
        dedoIndicador = estado[1]

        # Verifique se o dedo indicador mudou de estado
        if estado != estadoAtual and estado == [0, 1, 0, 0, 0]:
            print('Deslizar para cima (scroll para cima)')
            kb.press(Key.up)
            kb.release(Key.up)
        if estado != estadoAtual and estado == [0, 0, 0, 1, 0]:
            print('Deslizar para baixo (scroll para baixo)')
            kb.press(Key.down)
            kb.release(Key.down)

        if estado != estadoAtual and estado == [0, 0, 0, 0, 1]:
            print('passar slide')
            kb.press(Key.right)
            kb.release(Key.right)

        if estado != estadoAtual and estado == [1, 0, 0, 0, 0]:
            print('voltar slide')
            kb.press(Key.left)
            kb.release(Key.left)

        if estado == estadoAtual and estado == [0, 0, 0, 0, 1]:
            img[50:216, 984:1230] = setaDir
        if estado == estadoAtual and estado == [1, 0, 0, 0, 0]:
            img[50:216, 50:296] = setaEsq
        if estado == estadoAtual and estado == [0, 1, 0, 0, 0]:
            img[50:216, 300:546] = setaBai  # Exibe a seta "Bai" quando o dedo do meio está levantado
        if estado == estadoAtual and estado == [0, 0, 0, 1, 0]:
            img[50:216, 550:796] = setaCim  # Exibe a seta "Cim" quando o dedo anelar está levantado

        estadoAtual = estado

    cv2.imshow('img', cv2.resize(img, (640, 420)))
    cv2.waitKey(1)
