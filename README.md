Controle de Apresentações com Gestos de Mão
Este é um projeto que permite controlar apresentações de slides e rolar páginas usando gestos de mão, reconhecidos por uma câmera. O projeto utiliza Python com as bibliotecas OpenCV, cvzone, pynput e dlib para detectar gestos de mão e reconhecimento facial.

Pré-requisitos
Python 3.x
Bibliotecas OpenCV, cvzone, pynput, dlib (instaláveis via pip)
Câmera conectada ao computador
Como Usar
Clone o repositório ou baixe o script principal (controlador_apresentacao.py) e as imagens das setas para o mesmo diretório.

Certifique-se de ter as bibliotecas Python instaladas:
pip install opencv-python-headless
pip install cvzone
pip install pynput
pip install dlib

python controlador_apresentacao.py

Uma janela de vídeo deve ser exibida com o reconhecimento de gestos de mão. Use os seguintes gestos para controlar a apresentação:

Levante o dedo indicador para cima: Avançar slide
Levante o dedo indicador para baixo: Voltar slide
Levante o dedo médio: Role a página para baixo
Levante o dedo anelar: Role a página para cima
Para encerrar a execução do script, pressione Esc na janela do vídeo.

Notas
Certifique-se de que a câmera esteja conectada e funcione corretamente.
As imagens das setas (seta dir.PNG, seta esq.PNG, seta bai.PNG, seta cim.PNG) devem estar no mesmo diretório que o script principal.
O reconhecimento de piscadas de olhos requer o arquivo shape_predictor_68_face_landmarks.dat, que não está incluído no repositório. Você pode obter o arquivo em: (link para o arquivo do modelo do dlib).
