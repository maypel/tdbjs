from googlesearch import search

def get_google_results(query, num_results=10):
    results = []

    try:
        # Effectue la recherche et récupère les résultats
        for j in search(query, num_results=num_results):
            results.append({'link': j})

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    return results

# Exemple d'utilisation
if __name__ == "__main__":
    search_results = get_google_results("cours bitcoin")
    for result in search_results:
        print(result['link'])
