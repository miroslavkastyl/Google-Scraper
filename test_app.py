import unittest
from app import app

class TestGoogleScraper(unittest.TestCase):
    
    def setUp(self):
        # Vytvoříme si "virtuální prohlížeč" (test_client),
        # který umí posílat dotazy na náš server, aniž by běžel v prohlížeči.
        self.client = app.test_client()

    def test_homepage_loads(self):
        # Test 1: Kontrola, že se hlavní stránka vůbec načte.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Google Scraper', response.data)

    def test_search_output_format(self):
        # Test 2: Kontrola výstupu vyhledávání.
        response = self.client.post('/search', data={'keyword': 'Inizio'})
        self.assertEqual(response.status_code, 200)
        
        # Převedeme odpověď z JSONu na Python seznam (list)
        data = response.get_json()
        
        # Ověříme, že nám server poslal seznam a že má přesně 10 položek (Bod 3 zadání)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 10)
        
        # Ověříme, že výsledky mají správnou strukturu (obsahují 'titulek')
        self.assertIn('titulek', data[0])

if __name__ == '__main__':
    unittest.main()