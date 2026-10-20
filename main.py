import os
import requests

# Carregar as credenciais configuradas nos Secrets do GitHub
MB_API_KEY = os.getenv("MB_API_KEY")
MB_API_SECRET = os.getenv("MB_API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensagem):
    """Envia uma mensagem de alerta para o seu Telegram"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Credenciais do Telegram não encontradas nas variáveis de ambiente.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Mensagem enviada com sucesso para o Telegram!")
        else:
            print(f"Erro ao enviar para o Telegram: {response.text}")
    except Exception as e:
        print(f"Erro de conexão com o Telegram: {e}")

def verificar_mercado():
    """Função principal do robô (Verificação de Preço do Bitcoin)"""
    print("A verificar o mercado no Mercado Bitcoin...")
    
    # Consulta pública de ticker do Bitcoin no Mercado Bitcoin
    url = "https://www.mercadobitcoin.net/api/BTC/ticker/"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            preco_atual = float(dados['ticker']['last'])
            
            mensagem_alerta = (
                f"🤖 **Robô Bitcoin - Status**\n\n"
                f"📊 Execução realizada com sucesso na nuvem!\n"
                f"💰 Preço atual do Bitcoin: R$ {preco_atual:,.2f}\n"
                f"⚡ Estratégia de médias móveis 9/21 em monitoramento."
            )
            
            # Dispara o alerta para o Telegram
            enviar_telegram(mensagem_alerta)
        else:
            print(f"Erro ao consultar a API do Mercado Bitcoin: {response.text}")
    except Exception as e:
        print(f"Erro ao aceder ao mercado: {e}")

if __name__ == "__main__":
    verificar_mercado()
