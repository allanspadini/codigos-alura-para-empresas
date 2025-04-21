from typing import Any
import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("automacoes_web")

@mcp.tool()
def extrair_manchetes(url: str = "https://g1.globo.com") -> dict:
    """
    Extrai as principais manchetes de um site de notícias.
    
    Args:
        url: URL do site de notícias (padrão: g1.globo.com)
        
    Returns:
        Um dicionário com as principais manchetes encontradas
    """
    try:
        # Faz a requisição para o site
        response = requests.get(url)
        response.raise_for_status()
        
        # Parseia o HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrai os títulos - isso pode variar dependendo da estrutura do site
        # Aqui estamos buscando elementos que geralmente contêm manchetes
        titulos = []
        
        # Procura por elementos comuns que contêm manchetes
        for elemento in soup.find_all(['h1', 'h2', 'h3', '.headline', '.title']):
            if elemento.text.strip():
                titulos.append(elemento.text.strip())
        
        # Remove duplicatas e limita a 10 manchetes
        titulos = list(dict.fromkeys(titulos))[:10]
        
        return {
            "site": url,
            "quantidade": len(titulos),
            "manchetes": titulos
        }
    except Exception as e:
        return {"erro": str(e)}

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
