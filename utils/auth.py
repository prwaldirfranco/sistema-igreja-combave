import json
import os

CAMINHO_USUARIOS = "data/usuarios.json"

def carregar_usuarios():
    if os.path.exists(CAMINHO_USUARIOS):
        with open(CAMINHO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def verificar_credenciais(usuario, senha):
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario and u["senha"] == senha:
            return u  # retorna o dicionário completo
    return None
