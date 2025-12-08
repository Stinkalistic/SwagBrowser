import subprocess, argparse,requests,os

os.chdir(os.path.dirname(os.path.realpath(__file__)))
argparser=argparse.ArgumentParser(description="supre epic browser")
argparser.add_argument("-u","--url",help="tha url")
args=argparser.parse_args()

if os.path.exists("bookmarks.txt") and not args.url:
    with open("bookmarks.txt","r") as file:
        bookmarks=file.readlines()
        bookmarks = [b.strip() for b in bookmarks]
        titles=[b.split("||")[1] for b in bookmarks]
        bookmarks=[b.split("||")[0] for b in bookmarks]
        print("Your bookmarks:")
        for i in range(len(bookmarks)):
            print(f"{i+1}. {titles[i]} ({bookmarks[i]})")
        print("enter the number of a bookmark to open it\n")

if not args.url:
    url=input("enter website URL: \n")
else:
    url=args.url

if url.isdigit():
    url=int(url)
    if url>0 and url<=len(bookmarks):
        url=bookmarks[url-1]
    else:
        exit()

if not url.startswith("http"):
    url="https://"+url

try:
    r=requests.get(url)
    with open("html.html","w") as f:
        f.write(r.text)
except:
    subprocess.run("curl -L -s -o html.html "+url)
try:
    subprocess.run("py parser.py -i html.html -u "+url)
except:
    subprocess.run("python parser.py -i html.html -u "+url)
