import requests

def get_financial_summary():
    """
    Busca as cotações do Dólar, Euro e Bitcoin em uma única requisição HTTP.
    """
    try:
        dollar_info = get_dollar_price()
        euro_info = get_euro_price()
        pound_info = get_pound_price()
        bitcoin_info = get_bitcoin_price()

        summary = (
            "📊 **PAINEL DE COTAÇÕES**\n"
            "------------------------------------\n"
            f"{dollar_info}\n\n"
            f"{euro_info}\n\n"
            f"{pound_info}\n\n"
            f"{bitcoin_info}"
        )
        return summary
    except:
        return "Não foi possível obter as cotações no momento."

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

def get_euro_price():
    # URL da AwesomeAPI para cotação de Euro comercial (EUR-BRL)
    url = "https://economia.awesomeapi.com.br/last/EUR-BRL"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            eur_info = data["EURBRL"]
            
            # Extrai os dados em formato float
            bid = float(eur_info["bid"])    # Valor de Compra
            ask = float(eur_info["ask"])    # Valor de Venda
            high = float(eur_info["high"])  # Máxima do dia
            low = float(eur_info["low"])    # Mínima do dia
            
            return (
                f"💶 **Cotação do Euro (EUR/BRL)**\n\n"
                f"• **Compra:** R$ {bid:.2f}\n"
                f"• **Venda:** R$ {ask:.2f}\n"
                f"• **Máxima:** R$ {high:.2f}\n"
                f"• **Mínima:** R$ {low:.2f}"
            )
        else:
            return "Não foi possível obter a cotação no momento."
            
    except requests.exceptions.RequestException:
        return "Erro ao conectar com a API do euro."

def get_pound_price():
    # URL da AwesomeAPI para cotação de Libra esterlina comercial (GBP-BRL)
    url = "https://economia.awesomeapi.com.br/last/GBP-BRL"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            gbp_info = data["GBPBRL"]
            
            # Extrai os dados em formato float
            bid = float(gbp_info["bid"])    # Valor de Compra
            ask = float(gbp_info["ask"])    # Valor de Venda
            high = float(gbp_info["high"])  # Máxima do dia
            low = float(gbp_info["low"])    # Mínima do dia
            
            return (
                f"💷 **Cotação da Libra Esterlina (GBP/BRL)**\n\n"
                f"• **Compra:** R$ {bid:.2f}\n"
                f"• **Venda:** R$ {ask:.2f}\n"
                f"• **Máxima:** R$ {high:.2f}\n"
                f"• **Mínima:** R$ {low:.2f}"
            )
        else:
            return "Não foi possível obter a cotação no momento."
            
    except requests.exceptions.RequestException:
        return "Erro ao conectar com a API da libra esterlina."

def get_bitcoin_price():
    # URL da AwesomeAPI para cotação de Bitcoin (BTC-BRL)
    url = "https://economia.awesomeapi.com.br/last/BTC-BRL"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            btc_info = data["BTCBRL"]
            
            # Extrai os dados em formato float
            bid = float(btc_info["bid"])    # Valor de Compra
            ask = float(btc_info["ask"])    # Valor de Venda
            high = float(btc_info["high"])  # Máxima do dia
            low = float(btc_info["low"])    # Mínima do dia
            
            return (
                f"₿ **Cotação do Bitcoin (BTC/BRL)**\n\n"
                f"• **Compra:** R$ {bid:.2f}\n"
                f"• **Venda:** R$ {ask:.2f}\n"
                f"• **Máxima:** R$ {high:.2f}\n"
                f"• **Mínima:** R$ {low:.2f}"
            )
        else:
            return "Não foi possível obter a cotação no momento."
            
    except requests.exceptions.RequestException:
        return "Erro ao conectar com a API do bitcoin."
