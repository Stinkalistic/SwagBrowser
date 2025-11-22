import subprocess, argparse,requests,os

os.chdir(os.getcwd())
argparser=argparse.ArgumentParser(description="supre epic browser")
argparser.add_argument("-u","--url",help="tha url")
args=argparser.parse_args()

if not args.url:
    url=input("enter website URL: \n")
else:
    url=args.url

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
