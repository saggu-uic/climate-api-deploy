# download_lcz.py
import os
import requests

def download_file(url, output_path):
    if os.path.exists(output_path):
        print(f"{output_path} already exists. Skipping download.")
        return

    print(f"Downloading {url} to {output_path}")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded {output_path}")

if __name__ == "__main__":
    lcz_url = "https://drive.google.com/uc?export=download&id=1jRhT4mmmpUFeCmMGR_90nbdtNBz4v7B_"  # Replace with your actual file link
    lcz_path = "lcz_filter_v3.tif"
    download_file(lcz_url, lcz_path)
