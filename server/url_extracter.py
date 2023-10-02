import requests

from datetime import datetime
import time

import os

while True:

    output_directory = 'files'
    os.makedirs(output_directory, exist_ok=True)

    def get_current_timestamp():
        current_datetime = datetime.now()
        current_timestamp = int(current_datetime.timestamp())
        return current_timestamp

    def get_current_datetime():
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_datetime


    def fetch_m3u8_links(url):
        response = requests.get(url)
        response_text = response.text

        # Split the text by '
        split_text = response_text.split("'")

        # Filter the split_text to find the .m3u8 links
        m3u8_links = [link for link in split_text if link.endswith(".m3u8")]

        return m3u8_links

    northgate_link = ""
    southgate_link = ""
    try:
        m3u8_links = []
        with open(os.path.join(output_directory, "__NORTHGATE_STATUS"), "w") as f:
            # Usage example
            try:
                url = "http://wowza.ust.hk/Northgate/"
                m3u8_links = fetch_m3u8_links(url)

                if len(m3u8_links) != 1:
                    f.write(get_current_datetime() + " TOO MANY LINKS!")
                else:
                    northgate_link = m3u8_links[0]
                    f.write(get_current_datetime() + " OK: " + northgate_link)
                    with open(os.path.join(output_directory, "_NG.LINK"), "w") as f_link:
                        f_link.write(northgate_link)

            except Exception as e:
                f.write(get_current_datetime() + " NETWORK ERROR!")
    except:
        print(get_current_datetime() + " FILESYSTEM ERROR!")

    try:
        m3u8_links = []
        with open(os.path.join(output_directory, "__SOUTHGATE_STATUS"), "w") as f:
            # Usage example
            try:
                url = "http://wowza.ust.hk/Southgate/"
                m3u8_links = fetch_m3u8_links(url)

                if len(m3u8_links) != 1:
                    f.write(get_current_datetime() + " TOO MANY LINKS!")
                else:
                    southgate_link = m3u8_links[0]
                    f.write(get_current_datetime() + " OK: " + southgate_link)
                    with open(os.path.join(output_directory, "_SG.LINK"), "w") as f_link:
                        f_link.write(southgate_link)

            except Exception as e:
                f.write(get_current_datetime() + " NETWORK ERROR!")
    except:
        print(get_current_datetime() + " FILESYSTEM ERROR!")

    import subprocess
    import os

    def run_ffmpeg_command(input_url, output_file):
        output_directory = 'files'
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, output_file)

        command = [
            'ffmpeg',
            '-i', input_url,
            '-vf', 'select=eq(n\\,0)',
            '-vframes', '1',
            output_path,
            '-y'
        ]

        try:
            subprocess.run(command, check=True)
            print('Command executed successfully.')
        except subprocess.CalledProcessError as e:
            print(f'Error executing command: {e}')



    c_timestamp = get_current_timestamp()
    run_ffmpeg_command(northgate_link, f"NG-{c_timestamp}.jpg")

    run_ffmpeg_command(southgate_link, f"SG-{c_timestamp}.jpg")


    # FILE PURGING

    # Folder path
    folder_path = "files"

    # Threshold
    threshold = c_timestamp - 86400*7

    # Get all files in the folder
    files = os.listdir(folder_path)

    # Iterate over each file
    for file_name in files:
        # Check if the file starts with "NG-" or "SG-" and ends with ".jpg"
        if (file_name.startswith("NG-") or file_name.startswith("SG-")) and file_name.endswith(".jpg"):
            # Extract the integer from the file name
            try:
                integer = int(file_name.split(".")[0].split("-")[-1])
            except ValueError:
                integer = 0
            
            # Check if the integer is smaller than the threshold
            if integer < threshold:
                # Delete the file
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                print(f"Deleted file: {file_name}")

    for i in range(60):
        time.sleep(1)
        print("#"*i + " "*(60-i) + "|")