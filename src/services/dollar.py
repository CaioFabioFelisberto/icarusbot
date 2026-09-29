import requests

def get_dollar_price():
    # URL da AwesomeAPI para cotação de Dólar comercial (USD-BRL)
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            usd_info = data["USDBRL"]
            
            # Extrai os dados em formato float
            bid = float(usd_info["bid"])    # Valor de Compra
            ask = float(usd_info["ask"])    # Valor de Venda
            high = float(usd_info["high"])  # Máxima do dia
            low = float(usd_info["low"])    # Mínima do dia
            
            return (
                f"💵 **Cotação do Dólar (USD/BRL)**\n\n"
                f"• **Compra:** R$ {bid:.2f}\n"
                f"• **Venda:** R$ {ask:.2f}\n"
                f"• **Máxima:** R$ {high:.2f}\n"
                f"• **Mínima:** R$ {low:.2f}"
            )
        else:
            return "Não foi possível obter a cotação no momento."
            
    except requests.exceptions.RequestException:
        return "Erro ao conectar com a API do dólar."
    