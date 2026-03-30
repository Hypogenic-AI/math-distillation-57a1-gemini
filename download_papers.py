import requests
import os

def download_paper(url, filename):
    print(f"Downloading {url} to {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

if __name__ == "__main__":
    os.makedirs("papers", exist_ok=True)
    download_paper("https://arxiv.org/pdf/2512.07087.pdf", "papers/2512.07087_Equational_Theories_Project.pdf")
