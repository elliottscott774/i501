# Import necessary libraries
import requests
import os
import pandas as pd
from multiprocessing import Pool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Define the function to fetch data from the Genius API
def fetch_data_from_genius(search_term):
    base_url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = []
    
    try:
        # Make the request to the Genius API
        response = requests.get(base_url, headers=headers, params={'q': search_term})
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        
        # Process the results
        hits = response.json()['response']['hits']
        for hit in hits:
            song_data = {
                'search_term': search_term,
                'title': hit['result']['title'],
                'artist': hit['result']['primary_artist']['name']
            }
            data.append(song_data)
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError for {search_term}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"RequestException for {search_term}: {e}")
    except Exception as e:
        print(f"Unexpected error for {search_term}: {e}")
    
    return data

# Function to save results to a CSV file
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function to handle multiprocessing
def main(search_terms):
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(fetch_data_from_genius, search_terms)
        # Flatten the list of lists
        flat_results = [item for sublist in results for item in sublist]
        save_to_csv(flat_results, 'genius_data.csv')

if __name__ == "__main__":
    search_terms = ["Adele", "Drake", "BTS", "Mac Demarco", "Red Hot Chili Peppers","Smashmouth"]  # Example search terms
    main(search_terms)
