import os
from deepface import DeepFace

FACES_DIR = "faces_cadastradas"

def reconhecer_face(imagem_bytes: bytes):
    temp_path = "temp_captura.jpg"
    with open(temp_path, "wb") as f:
        f.write(imagem_bytes)

    for arquivo in os.listdir(FACES_DIR):
        if arquivo.endswith((".jpg", ".jpeg", ".png")):
            caminho = os.path.join(FACES_DIR, arquivo)
            try:
                resultado = DeepFace.verify(
                    img1_path=temp_path,
                    img2_path=caminho,
                    enforce_detection=False
                )
                if resultado["verified"]:
                    return arquivo.split(".")[0]
            except Exception:
                continue

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return None
