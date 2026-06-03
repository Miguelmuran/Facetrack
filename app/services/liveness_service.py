import cv2
import numpy as np
from PIL import Image
import io

def verificar_vivacidade(imagem_bytes: bytes) -> bool:
    imagem_pil = Image.open(io.BytesIO(imagem_bytes)).convert("RGB")
    imagem_np = np.array(imagem_pil)

    cinza = cv2.cvtColor(imagem_np, cv2.COLOR_RGB2GRAY)

    _, desvio = cv2.meanStdDev(cinza)
    desvio = desvio[0][0]

    laplaciano = cv2.Laplacian(cinza, cv2.CV_64F).var()

    if desvio > 30 and laplaciano > 100:
        return True

    return False
