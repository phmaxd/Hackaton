import cv2
import pickle
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
from sklearn.cluster import KMeans  # Import necessário para clusterização

# Abre janela para o usuário escolher a imagem do gabarito
root = tk.Tk()
root.withdraw()
gabarito_path = filedialog.askopenfilename(
    title="Selecione a imagem do gabarito",
    filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif")]
)

if not gabarito_path:
    print("Nenhuma imagem selecionada. Encerrando o programa.")
    exit()

# Carrega a imagem em escala de cinza
gabarito_img = cv2.imread(gabarito_path, cv2.IMREAD_GRAYSCALE)

# --- Processamento do gabarito correto ---
if gabarito_img is not None:
    print("Gabarito carregado em escala de cinza.")
    gabarito_blur = cv2.GaussianBlur(gabarito_img, (5, 5), 0)
    print("Filtro blur aplicado.")

    # Aplica binarização (threshold) para separar marcações do fundo
    _, gabarito_thresh = cv2.threshold(gabarito_blur, 127, 255, cv2.THRESH_BINARY_INV)
    print("Binarização aplicada.")

    # Aplica operações morfológicas para melhorar a separação dos quadrados
    kernel = np.ones((3, 3), np.uint8)
    gabarito_morph = cv2.morphologyEx(gabarito_thresh, cv2.MORPH_CLOSE, kernel)
    print("Morfologia aplicada.")

    # Encontra os contornos dos quadrados
    contours, _ = cv2.findContours(gabarito_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtra contornos por área e formato dos retângulos das alternativas
    min_area = 1500  # Ajustado para captar mais contornos
    max_area = 9000
    filtered_contours = []
    altura, largura = gabarito_img.shape

    # Limites para ignorar margens e letras (ajuste conforme necessário)
    limite_esquerda = int(largura * 0.15)
    limite_direita = int(largura * 0.85)
    limite_topo = int(altura * 0.03)
    limite_base = int(altura * 0.97)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect_ratio = float(w) / h
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)
        # Filtra apenas por área, aspecto e vértices
        if (min_area < area < max_area and
            1.8 < aspect_ratio < 3.2 and 4 <= len(approx) <= 6):
            filtered_contours.append(cnt)
    print(f"Contornos filtrados: {len(filtered_contours)}")

    # Calcula o centro (x, y) de cada quadrado filtrado
    centros = []
    for cnt in filtered_contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centros.append((cX, cY))

    # Se não houver centros suficientes, avisa e encerra
    if len(centros) < 2:
        print("Não foram detectados centros suficientes para formar colunas. Verifique a imagem do gabarito.")
        exit()

    # Agrupa centros em duas colunas usando KMeans
    centros_np = np.array(centros)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(centros_np[:, 0].reshape(-1, 1))
    labels = kmeans.labels_

    col1 = centros_np[labels == 0]
    col2 = centros_np[labels == 1]

    # Ordena cada coluna por Y (vertical)
    col1 = sorted(col1, key=lambda c: c[1])
    col2 = sorted(col2, key=lambda c: c[1])

    # Junta as linhas das duas colunas
    linhas = []
    for i in range(max(len(col1), len(col2))):
        linha = []
        if i < len(col1):
            linha.append(tuple(col1[i]))
        if i < len(col2):
            linha.append(tuple(col2[i]))
        linhas.append(linha)

    # Ordena cada linha por X (alternativas)
    for linha in linhas:
        linha.sort(key=lambda c: c[0])

    # (Opcional) Visualização para debug - comente se não quiser abrir janela
    # debug_img = cv2.cvtColor(gabarito_img, cv2.COLOR_GRAY2BGR)
    # for centro in centros:
    #     cv2.circle(debug_img, (int(centro[0]), int(centro[1])), 10, (0, 0, 255), 2)
    # cv2.imshow("Centros detectados", debug_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Verifica se cada quadrado está marcado
    raio = 18
    marcadas = []
    for linha in linhas:
        linha_marcada = []
        for centro in linha:
            mask = np.zeros_like(gabarito_thresh)
            cv2.circle(mask, centro, raio, 255, -1)
            media = cv2.mean(gabarito_thresh, mask=mask)[0]
            marcada = media < 80
            linha_marcada.append(marcada)
        marcadas.append(linha_marcada)

    # Monta a lista de respostas do gabarito correto
    respostas_gabarito = []
    for linha in marcadas:
        try:
            alternativa = linha.index(True)
        except ValueError:
            alternativa = None
        respostas_gabarito.append(alternativa)

    print("Respostas do gabarito correto (índice da alternativa marcada):")
    for i, resp in enumerate(respostas_gabarito):
        print(f"Pergunta {i+1}: {resp}")
else:
    print("Não foi possível carregar o gabarito oficial.")
    exit()

# --- Processamento do gabarito do aluno ---
aluno_path = filedialog.askopenfilename(
    title="Selecione a imagem do gabarito do aluno",
    filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif")]
)

if not aluno_path:
    print("Nenhuma imagem de aluno selecionada. Encerrando o programa.")
    exit()

aluno_img = cv2.imread(aluno_path, cv2.IMREAD_GRAYSCALE)

def processar_gabarito(img_gray, raio=18, limiar_marcacao=80):
    # Aplica blur
    blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    # Binarização inversa
    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)
    # Morfologia fechamento para unir regiões
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # Encontra contornos
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Filtra contornos por área, aspecto e vértices
    min_area = 1500
    max_area = 9000
    filtered_contours = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect_ratio = float(w) / h
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.03 * peri, True)
        if (min_area < area < max_area and
            1.8 < aspect_ratio < 3.2 and 4 <= len(approx) <= 6):
            filtered_contours.append(cnt)
    print(f"Contornos filtrados: {len(filtered_contours)}")
    if len(filtered_contours) < 2:
        print("Não foram detectados contornos suficientes para formar colunas.")
        return None, None
    # Calcula centros
    centros = []
    for cnt in filtered_contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centros.append((cX, cY))
    # Agrupa em 2 colunas com KMeans
    centros_np = np.array(centros)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(centros_np[:, 0].reshape(-1, 1))
    labels = kmeans.labels_
    col1 = centros_np[labels == 0]
    col2 = centros_np[labels == 1]
    col1 = sorted(col1, key=lambda c: c[1])
    col2 = sorted(col2, key=lambda c: c[1])
    linhas = []
    for i in range(max(len(col1), len(col2))):
        linha = []
        if i < len(col1):
            linha.append(tuple(col1[i]))
        if i < len(col2):
            linha.append(tuple(col2[i]))
        linhas.append(linha)
    for linha in linhas:
        linha.sort(key=lambda c: c[0])
    # Verifica marcações
    marcadas = []
    for linha in linhas:
        linha_marcada = []
        for centro in linha:
            mask = np.zeros_like(morph)
            cv2.circle(mask, centro, raio, 255, -1)
            media = cv2.mean(morph, mask=mask)[0]
            marcada = media < limiar_marcacao
            linha_marcada.append(marcada)
        marcadas.append(linha_marcada)
    respostas = []
    for linha in marcadas:
        try:
            alternativa = linha.index(True)
        except ValueError:
            alternativa = None
        respostas.append(alternativa)
    return respostas, linhas


# --- Processamento de múltiplos gabaritos de alunos ---
alunos_files = filedialog.askopenfilenames(
    title="Selecione os gabaritos dos alunos",
    filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif")]
)

if not alunos_files:
    print("Nenhum arquivo de aluno selecionado. Encerrando o programa.")
    exit()

for aluno_path in alunos_files:
    
    aluno_file = os.path.basename(aluno_path)
    aluno_img = cv2.imread(aluno_path, cv2.IMREAD_GRAYSCALE)
    if aluno_img is not None:
        aluno_blur = cv2.GaussianBlur(aluno_img, (5, 5), 0)
        _, aluno_thresh = cv2.threshold(aluno_blur, 127, 255, cv2.THRESH_BINARY_INV)
        
        respostas_aluno = []
        for linha in linhas:
            linha_marcada = []
            medias = []
            for centro in linha:
                mask = np.zeros_like(aluno_thresh)
                cv2.circle(mask, centro, raio, 255, -1)
                media = cv2.mean(aluno_thresh, mask=mask)[0]
                medias.append(media)
            limiar = np.median(medias) * 0.9  # limiar adaptativo
            for media in medias:
                marcada = media < limiar
                linha_marcada.append(marcada)
            marcadas_indices = [i for i, marcada in enumerate(linha_marcada) if marcada]
            if len(marcadas_indices) == 1:
                alternativa = marcadas_indices[0]
            else:
                alternativa = None
            respostas_aluno.append(alternativa)

        respostas_erradas = 0
        for resp_aluno, resp_gabarito in zip(respostas_aluno, respostas_gabarito):
            if resp_aluno != resp_gabarito:
                respostas_erradas += 1
        total_perguntas = len(respostas_gabarito)
        acertos = total_perguntas - respostas_erradas
        nota = acertos * 10

        print(f"\nAluno: {aluno_file}")
        print(f"Acertos: {acertos}")
        print(f"Erros: {respostas_erradas}")
        print(f"Nota final: {nota:.2f}")
    else:
        print(f"Não foi possível carregar o gabarito do aluno: {aluno_file}")
