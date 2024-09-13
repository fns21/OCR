Para este trabalho de classificação de placas de veículos através de reconhecimento óptico de caracteres, foi necessário a utilização prévia de algumas técnicas para tratamento e pré-processamento da imagem. Após a leitura da imagem em escala de cinza, ela passa por uma série de processos de aprimoramentos:
    -Redimensionamento;
    -Binarização da cor (Preto e Branco);
    -Inversão das cores;
    -Desfoque da imagem;
    -Aguçamento da imagem

Para o desfoque, que diminui o ruído da imagem, foi utilizado a biblioteca PILLOW ao invés da OpenCV, pois foi constatado uma melhora significativa no reconhecimento dos caracteres em 10% em relação ao OpenCV. Técnicas morfológicas como: Esqueletização, Dilação, Erosão, etc, foram usadas mas descartadas após colaborarem apenas com a redução do reconhecimento, contrário do desejado.

Após essa maratona de pré-processamento, a imagem é de fato enviada para a etapa de reconhecimento e isso ocorre com a biblioteca de OCR, Pytesseract. Isso resultou em aproximadamente 50% de reconhecimento. Entretanto nota-se que há muita confusão com letras parecidas com números e vice-versa, então foi feito um tratamento de string usando a ideia de LEET ou 1337. Para isso, sabendo que a string possui sua parte alfabética e numérica, para cada parte foi usado um dicionário específico com as trocas mais comuns que estavam ocorrendo. Isso elevou o reconhecimento para acima de 70%, para 100% dos caracteres, o que eu considerei satisfatório levando em consideração o enunciado do trabalho.

Por fim, ele classifica a placa como "boa" caso a string encontrada tenha até 2 caracteres de diferença quando comparado com o nome do arquivo ou "ruim" caso contrário. Para as ruins, cria-se um log dos caracteres que não foram reconhecidos. Com essa tolerância, o reconhecimento da placa atingiu 88%.

Fábio Naconeczny da Silva
