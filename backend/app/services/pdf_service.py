# PDF text extraction service
from langchain_community.document_loaders import PyPDFLoader
import os
from typing import Dict, List

async def extract_text_from_pdf(file_path: str, clean_up: bool = True) -> Dict[str, any]:
    """
    Extract text content from PDF file
    
    Args:
        file_path: Absolute path to the PDF file
        clean_up: Whether to delete the file after extraction (default: True)
    
    Returns:
        dict with full_text, pages (list), and page_count
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier PDF n'existe pas: {file_path}")
    
    if not file_path.lower().endswith('.pdf'):
        raise ValueError("Le fichier doit être au format PDF")
    
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        if not pages:
            raise Exception("Le PDF ne contient aucune page ou est vide")
        
        # Extraire le texte de chaque page
        page_contents = [page.page_content for page in pages]
        
        # Concaténer tout le texte avec séparateur de pages
        full_text = "\n\n--- Page Break ---\n\n".join(page_contents)
        
        return {
            "full_text": full_text,
            "pages": page_contents,
            "page_count": len(pages),
            "file_name": os.path.basename(file_path)
        }
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du PDF: {str(e)}")
    finally:
        # Nettoyage : supprimer le fichier temporaire si demandé
        if clean_up and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                # Log l'erreur mais ne pas propager pour ne pas masquer l'erreur principale
                print(f"Avertissement: Impossible de supprimer le fichier temporaire: {str(e)}")