import tkinter as tk
from tkinter import filedialog
from PIL import Image
from io import BytesIO
from PIL.ExifTags import TAGS
import requests,time,os,json, uuid
from sys import argv


    
def print_exif(file_path):
    ti_c = os.path.getctime(file_path)
    ti_m = os.path.getmtime(file_path)
    c_ti = time.ctime(ti_c)
    m_ti = time.ctime(ti_m)
    print(f"The file located at the path {file_path}\nwas created at {c_ti}\nand was last modified at {m_ti}")
    c_ti = time.strftime("%d:%m:%Y-%H:%M", time.localtime(ti_c))
    m_ti = time.strftime("%d/%m/%Y-%H:%M", time.localtime(ti_m))
    print(f"The file located at the path {file_path}\nwas created at {c_ti}\nand was last modified at {m_ti}")
    with Image.open(file_path) as img:
        exif_data = img.getexif()
    if exif_data:
        for tag,value in exif_data.items():
            tag_name = TAGS.get(tag,tag)
            if tag_name.startswith("XP") and isinstance(value,bytes):
                try:
                    value = value.decode("utf-16").rstrip("\x00")
                except UnicodeDecodeError:
                    pass 
            print(f"{tag_name}: {value}")
    else:
        print("no exif data found :(");
def img_data(file_path):
    m_ti = time.strftime("%d/%m/%Y-%H:%M", time.localtime(os.path.getmtime(file_path)))
    with Image.open(file_path) as img:
        
        return {"size":img.size,"format":img.format,"color_mode":img.mode,"date":m_ti}
def check_internet():
    try:
        response = requests.get("https://www.google.com",timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False   
def img_data_online(url):
    response = requests.get(url)
    response.raise_for_status()
    with Image.open(BytesIO(response.content)) as img:
        return {"size":img.size,"format":img.format,"color_mode":img.mode}
def print_exif_online(url):
    response = requests.get(url)
    response.raise_for_status()
    with Image.open(BytesIO(response.content)) as img:
        exif_data = img.getexif()
    if exif_data:
        for tag,value in exif_data.items():
            tag_name = TAGS.get(tag,tag)
            if tag_name.startswith("XP") and isinstance(value,bytes):
                try:
                    value = value.decode("utf-16").rstrip("\x00")
                except UnicodeDecodeError:
                    pass
            print(f"{tag_name}: {value}")
    else:
        print("no exif data found :(");
def check_url(url):
    try:
        response = requests.get(url,timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False
root = tk.Tk()
root.withdraw()
data = {}

# print the first dialog
print("Welcome to the GraphX file uploader!");
print("="*10)
print(" make sure this file has been downloaded")
print("from a trusted source")
print("="*10)
print("to load a file we need to find the file path or a url")
print("do you want to load a url or a local file?")
mode = ""
file_path=""
for n in range(len(argv)):
    if n!=0:
        mode="file"
        file_path = argv[n]
        continue
while True:
    if mode=="file": 
       break
    l=input("enter 'file', or 'url':")
    if l=="file" or l== "url":
        mode = l
        break
    else:
        print("invalid option selected, please try again")
if mode == "file":
    print("using file mode")
    print("the next dialog will let you pick a file")
    print("press any key to continue")
    if file_path == "":
        input()
        file_path = filedialog.askopenfilename(title="Select your image")
        if file_path:
            print("Selected file:",file_path)
        else:
            print("no file selected, exiting...")
            exit(0)

    # load the file path
    print("stripping data from image")
    print("data stripped from image: ")
    print()
    print_exif(file_path)
    data = img_data(file_path)
    data["file"] = file_path
else:
    print("using url mode")
    print("please enter the raw url of your image")
    print("it must end in a file extension eg")
    url = input("https://example.com/your_image.jpg\nEnter image: ")
    data["url"] = url
    if check_internet():
        if check_url(url):
            print("stripping data from image")
            print("data stripped from image: ")
            print()
            print_exif_online(url)
            data = img_data_online(url)
        else:
            print("url took to long to load, either the image")
            print("is too big or the image url is wrong.")
            exit(0)
    else:
        print("do you have internet?")
        exit(0)
print()
data["size"] = str(data["size"])
data["size"] = data["size"].replace("(","")
data["size"] = data["size"].replace(")","")
data["size"] = data["size"].replace(",","x")
data["size"] = data["size"].replace(" ","")
print("answer the questions below, use the found data for reference")
while True:
    data["title"] = input("Enter a title for your image: ").strip()
    if(data["title"] == "q"):
        exit(0)
    if len(data["title"]) > 30:
        print(f"that title is too long, the max length is 30 your title was {len(data["title"])}")
    else:
        break
data["description"] = input("Enter in a description for your image: ").strip()
data["tags"] = input("Enter some tags/keywords, seperate each tag/keyword with a comma\n you must include the brand of car and the type of gamemode, eg drift: ")
#clean the tags
print("Enter the name of the creator if you plan on uploading ")
data["creator"] = input("frequently try to use the same creator name: ")
data["game"] = input("what game is this from?: ")


# Load the existing JSON file
with open("./index.json", "r") as file:
    existing_data = json.load(file)

# Ensure the "images" key exists
if "images" not in existing_data:
    existing_data["images"] = {}

# Generate a unique ID and append the new data
new_id = str(uuid.uuid4())  # Generate a new unique ID
existing_data["images"][new_id] = data

# Write the updated data back to the file
with open("./index.json", "w") as file:
    json.dump(existing_data, file, indent=2)
