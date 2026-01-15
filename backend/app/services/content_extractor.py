# Content extraction from Wikipedia URL
import wikipedia
import requests
from urllib.parse import urlparse, unquote
import re

def get_wikipedia_content(url: str, language: str = "fr"):
    """
    Extract content from Wikipedia URL
    
    Args:
        url: Wikipedia article URL
        language: Wikipedia language code (default: "fr" for French)
    
    Returns:
        dict with title, content, url, and summary
    """
    # 1. Configuration du User-Agent (OBLIGATOIRE pour ne pas être bloqué)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "WikiSmartEdu/1.0 (Educational Project; contact@wikismartedu.com)"
    })
    wikipedia.requests = session
    
    # 2. Configuration de la langue
    wikipedia.set_lang(language)

    # 3. Extraction du titre via urllib
    parsed_url = urlparse(str(url))
    # On récupère la dernière partie du chemin (ex: /wiki/Intelligence_artificielle)
    raw_title = parsed_url.path.split("/")[-1]
    # On décode les caractères spéciaux (%20, etc) et on remplace _ par espace
    title = unquote(raw_title).replace("_", " ")

    try:
        # 4. Récupération de la page
        # auto_suggest=False évite que wikipedia devine une autre page si le titre est ambigu
        page = wikipedia.page(title, auto_suggest=False)
        return {
            "title": page.title,
            "content": page.content,
            "summary": page.summary,
            "url": page.url,
            "language": language
        }
    except wikipedia.exceptions.PageError:
        raise Exception(f"Page Wikipedia introuvable pour le titre: {title}")
    except wikipedia.exceptions.DisambiguationError as e:
        # Retourner les options pour permettre à l'utilisateur de choisir
        raise Exception(f"Titre ambigu. Veuillez préciser parmi ces options : {', '.join(e.options[:5])}")
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction Wikipedia: {str(e)}")