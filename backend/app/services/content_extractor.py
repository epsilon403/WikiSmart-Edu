#extracting content from Wikipedia articles
import wikipedia
import requests
from urllib.parse import urlparse, unquote
import re

def get_wikipedia_content(url: str, language: str = None):
    """
    Extract content from Wikipedia URL
    
    Args:
        url: Wikipedia article URL
        language: Wikipedia language code (optional, auto-detected from URL)
    
    Returns:
        dict with title, content, url, and summary
    """
    # 1. Parse URL to extract language and title
    parsed_url = urlparse(str(url))
    
    # Auto-detect language from URL (e.g., en.wikipedia.org -> "en")
    if language is None:
        hostname = parsed_url.netloc
        if 'wikipedia.org' in hostname:
            language = hostname.split('.')[0]  # Extract "en" from "en.wikipedia.org"
        else:
            language = "en"  # Default to English
    
    # 2. Configuration du User-Agent (OBLIGATOIRE pour ne pas être bloqué)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "WikiSmartEdu/1.0 (Educational Project; contact@wikismartedu.com)"
    })
    wikipedia.requests = session
    
    # 3. Configuration de la langue
    wikipedia.set_lang(language)

    # 4. Extraction du titre via urllib
    raw_title = parsed_url.path.split("/")[-1]
    title = unquote(raw_title).replace("_", " ")

    try:
        # 5. Récupération de la page
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
        raise Exception(f"Erreur lors de l'extraction Wikipedia: {str(e)}")# Temp change
