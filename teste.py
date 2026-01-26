def formatar_moeda(entrada):
    limpo = entrada.strip().replace('R$', '').replace(' ', '')
    
    if ',' in limpo and '.' in limpo:
        limpo = limpo.replace('.', '').replace(',', '.')
    
    elif ',' in limpo:
        limpo = limpo.replace(',', '.')
        

    elif '.' in limpo:
        partes = limpo.split('.')
        if len(partes[-1]) == 3:
            limpo = limpo.replace('.', '')

    return float(limpo)
def main():
    texto = input("Insira o valor (ex: R$ 1.250,50): ")
    try:
        valor = formatar_moeda(texto)
        print(f"Valor convertido para float: {valor}")
    except ValueError:
        print("Erro: Certifique-se de digitar um valor numérico válido.")

if __name__ == '__main__':
    main()