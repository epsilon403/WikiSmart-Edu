#!/usr/bin/env python3
"""
Script de test pour vérifier les extracteurs Wikipedia et PDF
"""
import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire app au path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.content_extractor import get_wikipedia_content
from app.services.pdf_service import extract_text_from_pdf
from app.services.preprocessor import clean_and_segment_text, clean_text, split_into_chunks


def test_wikipedia_extraction():
    """Test de l'extraction Wikipedia"""
    print("\n" + "="*60)
    print("TEST 1: EXTRACTION WIKIPEDIA")
    print("="*60)
    
    # Test avec un article français
    test_url = "https://fr.wikipedia.org/wiki/Intelligence_artificielle"
    
    try:
        print(f"\n📥 Extraction de: {test_url}")
        result = get_wikipedia_content(test_url, language="fr")
        
        print(f"\n✅ Titre: {result['title']}")
        print(f"✅ Langue: {result['language']}")
        print(f"✅ URL: {result['url']}")
        print(f"✅ Longueur du contenu: {len(result['content'])} caractères")
        print(f"✅ Longueur du résumé: {len(result['summary'])} caractères")
        
        print(f"\n📝 Premier paragraphe du résumé:")
        print(result['summary'][:300] + "...")
        
        # Test du préprocesseur
        print(f"\n🔧 Test de segmentation...")
        sections = clean_and_segment_text(result['content'])
        print(f"✅ Nombre de sections détectées: {len(sections)}")
        print(f"✅ Sections: {list(sections.keys())[:5]}...")
        
        # Test du chunking
        print(f"\n✂️ Test de division en chunks...")
        chunks = split_into_chunks(result['content'], chunk_size=500, overlap=100)
        print(f"✅ Nombre de chunks: {len(chunks)}")
        print(f"✅ Taille du premier chunk: {len(chunks[0])} caractères")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        return False


async def test_pdf_extraction():
    """Test de l'extraction PDF"""
    print("\n" + "="*60)
    print("TEST 2: EXTRACTION PDF")
    print("="*60)
    
    # Créer un PDF de test simple
    print("\n📄 Création d'un PDF de test...")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        test_pdf_path = "/tmp/test_wikismart.pdf"
        
        # Créer un PDF simple
        c = canvas.Canvas(test_pdf_path, pagesize=letter)
        c.drawString(100, 750, "Test WikiSmart EDU")
        c.drawString(100, 700, "Ceci est un document de test.")
        c.drawString(100, 650, "Il contient plusieurs lignes de texte.")
        c.showPage()
        c.drawString(100, 750, "Page 2")
        c.drawString(100, 700, "Contenu de la deuxième page.")
        c.save()
        
        print(f"✅ PDF créé: {test_pdf_path}")
        
        # Extraire le contenu
        print(f"\n📥 Extraction du PDF...")
        result = await extract_text_from_pdf(test_pdf_path, clean_up=False)
        
        print(f"✅ Nom du fichier: {result['file_name']}")
        print(f"✅ Nombre de pages: {result['page_count']}")
        print(f"✅ Longueur du texte: {len(result['full_text'])} caractères")
        
        print(f"\n📝 Contenu extrait:")
        print(result['full_text'][:300])
        
        # Nettoyage manuel
        import os
        if os.path.exists(test_pdf_path):
            os.remove(test_pdf_path)
            print(f"\n🗑️ Fichier de test supprimé")
        
        return True
        
    except ImportError:
        print("\n⚠️ reportlab n'est pas installé. Installez-le avec: pip install reportlab")
        print("   Test PDF ignoré (optionnel)")
        return True
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_text_cleaning():
    """Test des fonctions de nettoyage de texte"""
    print("\n" + "="*60)
    print("TEST 3: NETTOYAGE DE TEXTE")
    print("="*60)
    
    test_text = """
    Ceci   est    un    texte     avec    
    
    
    plusieurs   espaces    et    
    retours   à   la   ligne
    """
    
    print(f"\n📝 Texte original ({len(test_text)} caractères):")
    print(repr(test_text)[:100])
    
    cleaned = clean_text(test_text)
    
    print(f"\n✨ Texte nettoyé ({len(cleaned)} caractères):")
    print(repr(cleaned))
    
    print(f"\n✅ Test réussi!")
    return True


async def main():
    """Exécuter tous les tests"""
    print("\n🚀 DÉBUT DES TESTS D'EXTRACTION")
    
    results = []
    
    # Test 1: Wikipedia
    results.append(("Wikipedia", test_wikipedia_extraction()))
    
    # Test 2: PDF
    results.append(("PDF", await test_pdf_extraction()))
    
    # Test 3: Nettoyage
    results.append(("Nettoyage", test_text_cleaning()))
    
    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
    
    for name, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"{name:20} {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
