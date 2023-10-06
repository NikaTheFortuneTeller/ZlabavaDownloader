import requests
import os
import concurrent.futures
from tqdm import tqdm
import pyfiglet

def download_file(url, destination_folder="."):
    try:
        # Extract the file name from the URL
        file_name = url.split("/")[-1]
        
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
    "https://f81.megaup.net/1fGe3/The.Sims.4.Horse.Ranch-RUNE.part01.rar?download_token=6d14762e36660ba357d375669630895bac510c0dd5f59aa0ca23d7daf8a85f99",
    "https://f82.megaup.net/1fGe5/The.Sims.4.Horse.Ranch-RUNE.part02.rar?download_token=82fa846b55242c78b7b02c4622be233426a8c4405a83fb25c463e8ef8be0e37c", 
    "https://f83.megaup.net/1fGe0/The.Sims.4.Horse.Ranch-RUNE.part03.rar?download_token=64adc0ef81d536cabc6227cff78de869b973e97077b5f34670e9a7efa7e90e74",
    "https://f15.megaup.net/2BB8D/The.Sims.4.Horse.Ranch-RUNE.part04.rar?download_token=be10b97eddde61bc061dbacc70db79f6a491752e22b3739b161a6c91d0ce9d7f",
    "https://f84.megaup.net/2BB8B/The.Sims.4.Horse.Ranch-RUNE.part05.rar?download_token=bc89fe2ae6f62167b0feb97cfa00d7af4e793cefe32df5a3d8fcbd7576765ff0", 
    "https://f79.megaup.net/1fGe1/The.Sims.4.Horse.Ranch-RUNE.part06.rar?download_token=e5af410a2b43c1e053134f36832917ca1cdccafc6d354e6b5107626b3c36b895",
    "https://f29.megaup.net/1fGe8/The.Sims.4.Horse.Ranch-RUNE.part07.rar?download_token=dc900997ecf30f2c5af048723b351d4fe0826c73bbab98d59627bd0ab3725b9c",
    "https://f77.megaup.net/2BB8A/The.Sims.4.Horse.Ranch-RUNE.part08.rar?download_token=a9649e42831fc47de710f4cf44bd43db711d1e7d48059e5c6fed36701b5d4e52",
    "https://f69.megaup.net/1fGe7/The.Sims.4.Horse.Ranch-RUNE.part09.rar?download_token=3ed98a3ce6e7212b3511d9812a4860a5a3280df164ffa4804f37e09ebd3ba65a",
    "https://f80.megaup.net/1fGe6/The.Sims.4.Horse.Ranch-RUNE.part10.rar?download_token=60c895e9c28acc3e7781cc237d0b82ec1211c14f8becbc77a9b44ac16a0e6e60", 
    "https://f78.megaup.net/1fGec/The.Sims.4.Horse.Ranch-RUNE.part11.rar?download_token=c8802bca474e9122c4458218343ebff73e05c39eca940905c3b2045769ec0264",
    "https://f62.megaup.net/1fGdt/The.Sims.4.Horse.Ranch-RUNE.part12.rar?download_token=a9a1a61eb20a7ed86b5da47bbe118790252223eaf1624c9976f0f39bb5d29a94"  
]

os.system("cls")
# Call the totally useful figlet banner thing muhahah
print(pyfiglet.figlet_format("Zlabava Downloader"))
print("v1.0 Designed in California - Made in China")

# Call the download_links function
download_links(download_links_list)
# os.system("del .\downloaded_files\download_log.txt") # Perfect solution xD
# os.system("type 'SMRADLAVEJ SOUBOR' > .\downloaded_files\download_log.txt")