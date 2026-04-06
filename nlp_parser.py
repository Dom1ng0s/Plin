import spacy
import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    logger.error("Modelo pt_core_news_sm não encontrado. Verifique o Dockerfile.")
    nlp = None

# Ampliamos a lista para incluir as formas conjugadas comuns.
# Como o texto é informal, o lematizador do modelo sm pode falhar em descobrir a raiz.
PALAVRAS_DESPESA = {"gastar", "gastei", "gastou", "comprar", "comprei", "pagar", "paguei", "perder", "torrar", "torrei", "deixar", "deixei", "custar", "custou","perdi","dei","doei","custaram","cobraram"}
PALAVRAS_RECEITA = {"receber", "recebi", "ganhar", "ganhei", "achar", "achei", "depositar", "render", "faturar", "faturei","pagaram","deram","doaram", }

PALAVRAS_IGNORADAS = {"real", "reais", "conto", "prata", "r$", "dinheiro", "pila", "hoje", "ontem", "agora"}

def extrair_valor_flexivel(texto: str) -> Optional[float]:
    """
    Captura números em vários formatos: 50.50, 1500, 120,00, 1.250,50
    """
    # Encontra qualquer sequência que pareça um número com pontos ou vírgulas
    padrao = r'(?:\b\d{1,3}(?:\.\d{3})+(?:,\d{2})?|\b\d+(?:[.,]\d{1,2})?)(?!\d)'
    matches = re.findall(padrao, texto)
    
    if not matches:
        return None
        
    valor_str = matches[0] # Pega o primeiro número encontrado
    
    if ',' in valor_str and '.' in valor_str:
        valor_str = valor_str.replace('.', '').replace(',', '.')
    elif ',' in valor_str:
        valor_str = valor_str.replace(',', '.')
        
    try:
        return float(valor_str)
    except ValueError:
        return None

def analisar_mensagem(texto: str) -> Optional[Dict[str, Any]]:
    if not nlp:
        return None

    valor = extrair_valor_flexivel(texto)
    if valor is None:
        return None

    doc = nlp(texto.lower())
    
    tipo_transacao = None
    entidades_categoria = []

    for token in doc:
        palavra = token.lower_
        lemma = token.lemma_
        
        # 1. Regra de Ouro (Inversão de Polaridade / Exceções)
        # Se a palavra for "pagaram", "devolveram", "reembolsaram" 
        # OU se for "pagou" antecedido da palavra "me" (ex: "me pagou")
        if palavra in ["pagaram", "devolveram", "reembolsaram"] or \
           (palavra == "pagou" and token.i > 0 and doc[token.i - 1].lower_ == "me"):
            tipo_transacao = "receita"
            continue # Pula o resto das regras para esta palavra

        # 2. Intenção Padrão
        if palavra in PALAVRAS_DESPESA or lemma in PALAVRAS_DESPESA:
            # Só marca como despesa se uma regra de ouro não tiver forçado receita antes
            if tipo_transacao != "receita":
                tipo_transacao = "despesa"
                
        elif palavra in PALAVRAS_RECEITA or lemma in PALAVRAS_RECEITA:
            tipo_transacao = "receita"

        # 3. Categoria: Estratégia de Eliminação
        elif not token.is_punct and not token.like_num and not token.is_stop:
            if palavra not in PALAVRAS_IGNORADAS and palavra not in PALAVRAS_DESPESA and palavra not in PALAVRAS_RECEITA:
                # Evita adicionar "me" como categoria quando usamos "me pagaram"
                if palavra != "me": 
                    entidades_categoria.append(token.text.capitalize())

    if not tipo_transacao:
        return None

    categoria = " ".join(entidades_categoria) if entidades_categoria else "Geral"
    valor_final = -abs(valor) if tipo_transacao == "despesa" else abs(valor)

    return {
        "tipo_transacao": tipo_transacao,
        "valor": valor_final,
        "categoria": categoria
    }

