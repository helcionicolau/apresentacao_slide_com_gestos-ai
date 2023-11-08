import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
import dlib

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

# Inicialize o detector de rosto
detectorFace = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Função para calcular o EAR do olho
def eye_aspect_ratio(eye):
    vertical_dist = cv2.norm(eye[1] - eye[5])
    horizontal_dist = cv2.norm(eye[0] - eye[3])
    ear = vertical_dist / (2.0 * horizontal_dist)
    return ear

# Variáveis para rastrear o estado dos olhos
contadorOlhoEsquerdo = 0
contadorOlhoDireito = 0

while True:
    _, img = video.read()
    hands, img = detector.findHands(img)

    # Converta a imagem em escala de cinza para a detecção de rosto
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detectar rosto
    faces = detectorFace(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        
        # Calcule o EAR para o olho esquerdo e direito
        ear_left = eye_aspect_ratio(landmarks[42:48])
        ear_right = eye_aspect_ratio(landmarks[36:42])

        # Verifique o piscar dos olhos com base no EAR
        if ear_left < 0.2:
            contadorOlhoEsquerdo += 1
        else:
            contadorOlhoEsquerdo = 0

        if ear_right < 0.2:
            contadorOlhoDireito += 1
        else:
            contadorOlhoDireito = 0

        # Se o olho esquerdo piscou duas vezes, avance o slide
        if contadorOlhoEsquerdo == 2:
            print('Olho esquerdo piscou duas vezes (avançar slide)')
            kb.press(Key.right)
            kb.release(Key.right)

        # Se o olho direito piscou duas vezes, volte o slide
        if contadorOlhoDireito == 2:
            print('Olho direito piscou duas vezes (voltar slide)')
            kb.press(Key.left)
            kb.release(Key.left)

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
