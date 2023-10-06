import requests
import os
import concurrent.futures
from tqdm import tqdm
import pyfiglet
from urllib.parse import urlparse

def get_valid_filename(url):
    # Parse the URL and get the file name
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)

    # Remove query parameters from the file name
    file_name = file_name.split('?')[0]
    return file_name

def download_file(url, destination_folder="."):
    try:
        # Get the clean file name from the URL
        file_name = get_valid_filename(url)
        
        # Prepare the destination file path
        destination_path = os.path.join(destination_folder, file_name)

        # Send an HTTP GET request to the URL
        response = requests.get(url, stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the total file size (if available in the response headers)
            total_size = int(response.headers.get('content-length', 0))

            # Open the file for binary write
            with open(destination_path, 'wb') as f:
                # Initialize the loading bar
                with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc=file_name) as pbar:
                    # Download the file in chunks to save memory
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        pbar.update(len(chunk))

            print(f"Download of {file_name} complete!")
            return True
        else:
            print(f"Failed to download {file_name}. Status Code: {response.status_code}")
            return False

    except Exception as e:
        print(f"An error occurred while downloading {file_name}: {str(e)}")
        return False

def download_links(download_links, destination_folder="downloaded_files", max_concurrent=3):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Load the completed downloads from the log file
    completed_downloads = set()
    log_file = os.path.join(destination_folder, "download_log.txt")
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            completed_downloads = set(f.read().splitlines())

    # Filter out completed downloads from the list
    download_links = [link for link in download_links if link not in completed_downloads]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        # Download each file from the specified links
        futures = {executor.submit(download_file, link, destination_folder): link for link in download_links}
        for future in concurrent.futures.as_completed(futures):
            link = futures[future]
            if future.result():
                # If download is successful, add the link to completed_downloads
                completed_downloads.add(link)
                # Write the completed link to the log file
                with open(log_file, "a") as f:
                    f.write(link + "\n")

# Specify the list of links to download
download_links_list = [
    "https://soundboardio.aquasoup.com/jolanda/zamicham-na-vas-vas-osud.mp3",
    "https://soundboardio.aquasoup.com/jolanda/a-chci-abyste-videli-jak-sem-zkusena.mp3",
    "https://soundboardio.aquasoup.com/jolanda/ano-mluvte-do-telefonu.mp3",
    "https://soundboardio.aquasoup.com/jolanda/dneska-opet-zijeme.mp3",
    "https://soundboardio.aquasoup.com/jolanda/halo.mp3",
    "https://soundboardio.aquasoup.com/jolanda/dobry-vecer.mp3",
    "https://soundboardio.aquasoup.com/jolanda/ha-jedeme.mp3",
    "https://soundboardio.aquasoup.com/jolanda/hodne-budes-nekde.mp3",
    "https://soundboardio.aquasoup.com/jolanda/chcete-volat-nechcete-volat-volejte-necekejte.mp3",
    "https://soundboardio.aquasoup.com/jolanda/i-ten-spatnej-clovek-na-kazdyho-spadne.mp3",
    "https://soundboardio.aquasoup.com/jolanda/moje-jmeno-je-jolanda.mp3",
    "https://soundboardio.aquasoup.com/jolanda/muzete-polozit-jenom-jednu-a-odpovim-vam-jenom-tri.mp3",
    "https://soundboardio.aquasoup.com/jolanda/nejsem-nejaky-medium.mp3",
    "https://soundboardio.aquasoup.com/jolanda/nenechte-se-zmat.mp3",
    "https://soundboardio.aquasoup.com/jolanda/tak-jaj-budoucnost.mp3",
    "https://soundboardio.aquasoup.com/jolanda/vidim-slysim-a-posloucham.mp3"
]


os.system("cls")
# Call the totally useful figlet banner thing muhahah
print(pyfiglet.figlet_format("Zlabava Downloader"))
print("v1.0 Designed in California - Made in China")

# Call the download_links function
download_links(download_links_list)
# os.system("del .\downloaded_files\download_log.txt") # Perfect solution xD
# os.system("type 'SMRADLAVEJ SOUBOR' > .\downloaded_files\download_log.txt")
