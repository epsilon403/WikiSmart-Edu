# Text preprocessing: section segmentation and text cleaning
import re
from typing import Dict, List

def clean_and_segment_text(raw_text: str) -> Dict[str, str]:
    """
    Segmente l'article en sections basées sur les structures de paragraphes.
    La librairie wikipedia retourne du texte déjà formaté sans les == ==
    
    Returns:
        Dictionnaire avec les sections { "Introduction": "texte...", "Section1": "texte..." }
    """
    sections = {}
    current_section = "Introduction"
    sections[current_section] = []

    # Pattern pour détecter les titres de section dans le texte Wikipedia API
    # Les titres sont généralement sur une ligne seule, suivis de paragraphes
    lines = raw_text.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        # Détecter un titre de section:
        # - Ligne courte (< 100 caractères)
        # - Commence par une majuscule
        # - Ne se termine pas par un point
        # - N'est pas tout en majuscules (acronyme)
        # - Suivie d'une ligne vide ou d'un paragraphe
        if (len(line) < 100 and 
            line[0].isupper() and 
            not line.endswith('.') and 
            not line.endswith(',') and
            not line.isupper() and
            '\n\n' in raw_text[max(0, raw_text.find(line)-5):raw_text.find(line)+len(line)+5]):
            
            # Nouveau titre de section détecté
            current_section = line
            sections[current_section] = []
        else:
            # Contenu de la section actuelle
            sections[current_section].append(line)

    # Reconvertir les listes en paragraphes
    result = {k: " ".join(v).strip() for k, v in sections.items() if v and " ".join(v).strip()}
    
    # Si aucune section détectée, retourner tout le texte comme introduction
    if not result or (len(result) == 1 and "Introduction" in result and not result["Introduction"]):
        result = {"Content": raw_text.strip()}
    
    return result


def clean_text(text: str) -> str:
    """
    Nettoie le texte en enlevant les espaces multiples, caractères spéciaux, etc.
    """
    # Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    
    # Supprimer les retours à la ligne multiples
    text = re.sub(r'\n+', '\n', text)
    
    return text.strip()


def split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Divise le texte en chunks pour le traitement par LLM
    
    Args:
        text: Texte à diviser
        chunk_size: Taille maximum de chaque chunk en caractères
        overlap: Nombre de caractères de chevauchement entre chunks
    
    Returns:
        Liste de chunks de texte
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Essayer de couper à une fin de phrase
        if end < len(text):
            # Chercher le dernier point avant la fin du chunk
            last_period = text.rfind('.', start, end)
            if last_period > start:
                end = last_period + 1
        
        chunks.append(text[start:end].strip())
        start = end - overlap if end < len(text) else end
    
    return chunks