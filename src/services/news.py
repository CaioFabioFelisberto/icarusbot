import asyncio
from playwright.async_api import async_playwright

async def get_latest_news():
    async with async_playwright() as p:
        # Lança o navegador em modo headless (sem interface gráfica)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.route(
            "**/*.{png,jpg,jpeg,svg,gif,webp,css,woff,woff2}", 
            lambda route: route.abort()
        )
        
        try:
            # Acede ao site de notícias
            await page.goto("https://g1.globo.com/", timeout=15000, wait_until="domcontentloaded")
            
            # Aguarda a presença dos elementos de manchete
            await page.wait_for_selector(".feed-post-link", timeout=5000)
            
            # Extrai os títulos e links dos primeiros 5 destaques
            news_elements = await page.query_selector_all(".feed-post-link")
            news_list = []
            
            for elem in news_elements[:5]:
                title = await elem.inner_text()
                url = await elem.get_attribute("href")
                if title and url:
                    news_list.append(f"📰 **{title.strip()}**\n🔗 [Ler notícia]({url})")
            
            await browser.close()
            
            if news_list:
                return "\n\n".join(news_list)
            return "Não foi possível encontrar notícias no momento."

        except Exception as e:
            await browser.close()
            return f"Ocorreu um erro ao buscar as notícias. {str(e)}"