import cv2
import pickle
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
from sklearn.cluster import KMeans  # Import necessário para clusterização

def corrigir_perspectiva(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return img
    contorno_maior = max(contours, key=cv2.contourArea)
    peri = cv2.arcLength(contorno_maior, True)
    approx = cv2.approxPolyDP(contorno_maior, 0.02 * peri, True)
    if len(approx) == 4:
        pts = approx.reshape(4, 2)
        # Ordenar pontos: superior-esquerdo, superior-direito, inferior-direito, inferior-esquerdo
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        (tl, tr, br, bl) = rect
        larguraA = np.linalg.norm(br - bl)
        larguraB = np.linalg.norm(tr - tl)
        alturaA = np.linalg.norm(tr - br)
        alturaB = np.linalg.norm(tl - bl)
        largura_max = max(int(larguraA), int(larguraB))
        altura_max = max(int(alturaA), int(alturaB))
        dst = np.array([
            [0, 0],
            [largura_max - 1, 0],
            [largura_max - 1, altura_max - 1],
            [0, altura_max - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(img, M, (largura_max, altura_max))
        return warped
    else:
        return img  # Retorna original se não encontrar 4 cantos

# --- Abre janela para o usuário escolher a imagem do gabarito ---
root = tk.Tk()
root.withdraw()
gabarito_path = filedialog.askopenfilename(
    title="Selecione a imagem do gabarito",
    filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif")]
)

if not gabarito_path:
    print("Nenhuma imagem selecionada. Encerrando o programa.")
    exit()

# Carrega a imagem colorida para correção de perspectiva
gabarito_img_color = cv2.imread(gabarito_path)
if gabarito_img_color is None:
    print("Não foi possível carregar a imagem do gabarito.")
    exit()

# Corrige perspectiva e converte para cinza
gabarito_img_corrigido = corrigir_perspectiva(gabarito_img_color)
gabarito_img = cv2.cvtColor(gabarito_img_corrigido, cv2.COLOR_BGR2GRAY)

# --- Processamento do gabarito correto ---
if gabarito_img is not None:
    print("Gabarito carregado e corrigido em escala de cinza.")
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

    # Calcula o centro (x, y) de cada quadrado filtrado
    centros = []
    for cnt in filtered_contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centros.append((cX, cY))

    if len(centros) < 2:
        print("Não foram detectados centros suficientes para formar colunas. Verifique a imagem do gabarito.")
        exit()

    # Agrupa centros em duas colunas usando KMeans
    centros_np = np.array(centros)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(centros_np[:, 0].reshape(-1, 1))
    labels = kmeans.labels_

    col1 = centros_np[labels == 0]
    col2 = centros_np[labels == 1]

    # Garante que col1 seja a coluna da esquerda e col2 a da direita
    if np.mean(col1[:, 0]) > np.mean(col2[:, 0]):
        col1, col2 = col2, col1

    # Ordena cada coluna por Y (vertical)
    col1 = sorted(col1, key=lambda c: c[1])
    col2 = sorted(col2, key=lambda c: c[1])

    # Agrupa alternativas por linha dentro de cada coluna
    def agrupar_por_linha(coluna, tolerancia_y=30):
        if not coluna:
            return []
        
        coluna_ordenada = sorted(coluna, key=lambda c: c[1])
        linhas = []
        linha_atual = [coluna_ordenada[0]]
        
        for i in range(1, len(coluna_ordenada)):
            if abs(coluna_ordenada[i][1] - linha_atual[-1][1]) <= tolerancia_y:
                linha_atual.append(coluna_ordenada[i])
            else:
                # Ordena a linha atual por X (alternativas A, B, C, D, E)
                linha_atual.sort(key=lambda c: c[0])
                linhas.append(linha_atual)
                linha_atual = [coluna_ordenada[i]]
        
        # Adiciona a última linha
        linha_atual.sort(key=lambda c: c[0])
        linhas.append(linha_atual)
        return linhas

    linhas_col1 = agrupar_por_linha(col1)
    linhas_col2 = agrupar_por_linha(col2)
    
    # Combina as linhas: primeiro todas da coluna 1, depois todas da coluna 2
    todas_linhas = linhas_col1 + linhas_col2
    
    print(f"Total de questões detectadas: {len(todas_linhas)}")
    print(f"Questões na coluna 1: {len(linhas_col1)}")
    print(f"Questões na coluna 2: {len(linhas_col2)}")

    raio = 18
    marcadas = []
    for linha in todas_linhas:
        linha_marcada = []
        for centro in linha:
            mask = np.zeros_like(gabarito_thresh)
            cv2.circle(mask, centro, raio, 255, -1)
            media = cv2.mean(gabarito_thresh, mask=mask)[0]
            marcada = media < 80
            linha_marcada.append(marcada)
        marcadas.append(linha_marcada)

    respostas_gabarito = []
    for linha in marcadas:
        try:
            alternativa = linha.index(True)
        except ValueError:
            alternativa = None
        respostas_gabarito.append(alternativa)

    print("Respostas do gabarito correto (índice da alternativa marcada):")
    for i, resp in enumerate(respostas_gabarito):
        coluna = "Col1" if i < len(linhas_col1) else "Col2"
        questao_na_coluna = (i % len(linhas_col1)) + 1 if i < len(linhas_col1) else (i - len(linhas_col1)) + 1
        print(f"Questão {i+1} ({coluna}-Q{questao_na_coluna}): {resp}")
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

aluno_img_color = cv2.imread(aluno_path)
if aluno_img_color is None:
    print("Não foi possível carregar a imagem do aluno.")
    exit()

aluno_img_corrigido = corrigir_perspectiva(aluno_img_color)
aluno_img = cv2.cvtColor(aluno_img_corrigido, cv2.COLOR_BGR2GRAY)

aluno_blur = cv2.GaussianBlur(aluno_img, (5, 5), 0)
_, aluno_thresh = cv2.threshold(aluno_blur, 127, 255, cv2.THRESH_BINARY_INV)

marcadas_aluno = []
for linha in todas_linhas:  # Usa a mesma estrutura de linhas do gabarito
    linha_marcada = []
    for centro in linha:
        mask = np.zeros_like(aluno_thresh)
        cv2.circle(mask, centro, raio, 255, -1)
        media = cv2.mean(aluno_thresh, mask=mask)[0]
        marcada = media < 80
        linha_marcada.append(marcada)
    marcadas_aluno.append(linha_marcada)

respostas_aluno = []
for linha in marcadas_aluno:
    try:
        alternativa = linha.index(True)
    except ValueError:
        alternativa = None
    respostas_aluno.append(alternativa)

# Normaliza tamanho das respostas do aluno para evitar desalinhamento
if len(respostas_aluno) < len(respostas_gabarito):
    respostas_aluno += [None] * (len(respostas_gabarito) - len(respostas_aluno))
elif len(respostas_aluno) > len(respostas_gabarito):
    respostas_aluno = respostas_aluno[:len(respostas_gabarito)]

print("\nRespostas do aluno e comparação:")
respostas_erradas = 0
for i, (resp_aluno, resp_gabarito) in enumerate(zip(respostas_aluno, respostas_gabarito), 1):
    status = "Correta" if resp_aluno == resp_gabarito else "Errada"
    coluna = "Col1" if i-1 < len(linhas_col1) else "Col2"
    questao_na_coluna = ((i-1) % len(linhas_col1)) + 1 if i-1 < len(linhas_col1) else ((i-1) - len(linhas_col1)) + 1
    print(f"Questão {i} ({coluna}-Q{questao_na_coluna}): Aluno = {resp_aluno}, Gabarito = {resp_gabarito} -> {status}")
    if resp_aluno != resp_gabarito:
        respostas_erradas += 1

total_perguntas = len(respostas_gabarito)
acertos = total_perguntas - respostas_erradas
nota = acertos * 10 / total_perguntas

print(f"\nResultado do aluno:")
print(f"Acertos: {acertos} de {total_perguntas}")
print(f"Erros: {respostas_erradas}")
print(f"Nota final: {nota:.2f}")