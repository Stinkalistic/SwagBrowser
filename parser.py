from html.parser import HTMLParser
from cmu_graphics import *
import argparse,subprocess,os,requests
linkopener=1
if not linkopener:
    import webbrowser as web

app.lt=""
app.y=10
app.x=20
app.elements=[]
app.indented=False
app.yold=10
app.attrs=[]
app.lastimg=""
app.lastsnd=""
src=""

try:
    with open("settings.cfg","r") as cfg:
        lines=cfg.readlines()
        lines=[line.split("=")[1].strip() for line in lines]
        app.scrollspeed=int(lines[1])
        app.textcolor=lines[3]
        app.background=lines[2]
        if lines[0].lower()=="true":
            app.background=rgb(55,55,69)
            app.textcolor="white"        
except:
    print("failed to load settings.cfg, using default settings")
    app.scrollspeed=5
    app.textcolor="black"

argparser = argparse.ArgumentParser(description='super epic html parser')
argparser.add_argument('-i',"--input", help='Path to the input file.')
argparser.add_argument("-u","--url",help="")
args=argparser.parse_args()

if args.url:
    title=args.url.removeprefix("https://").removeprefix("http://")
    try:
        if args.url.endswith(".htm"):
            app.elements.append(Image(os.path.basename(args.url)+"/favicon.ico",app.x-10,app.y))
        else:
            app.elements.append(Image(args.url+"/favicon.ico",app.x-10,app.y))
        app.y+=(app.elements[-1].bottom-app.elements[-1].top)+10
    except:
        print(args.url+"/favicon.ico")
        print("failed to load favicon")
    
try:
    print("Accessing file from "+args.url)
except:
    pass

def left():
    if app.indented:
        app.elements[-1].left=app.x+20
    else:
        app.elements[-1].left=app.x
    app.x=app.elements[-1].right+10

            
class MyHTMLParser(HTMLParser):
    def handle_starttag(self,tag,attrs):
        app.lt=tag
        app.attrs=attrs
        if tag=="br":
            app.y+=15
            app.x=20
        elif tag=="hr":
            app.y+=20
            app.elements.append(Line(5,app.y,395,app.y,fill="grey",lineWidth=1))
            app.y+=20
            app.x=20
    
    def handle_endtag(self,tag):
        if tag=="ul" and app.indented:
            app.indented=False
        
        
    def handle_data(self,data):
        global src,title
        if app.lt=="text":
            app.elements.append(Label(data,app.x,app.y,fill=app.textcolor))
            left()
        elif app.lt=="p":
            app.y+=20
            app.elements.append(Label(data,app.x,app.y,fill=app.textcolor))
            left()
            app.y+=20
        elif app.lt=="h1":
            app.y+=30
            app.elements.append(Label(data,app.x,app.y,size=20,bold=True,fill=app.textcolor))
            left()
            app.y+=10
        elif app.lt=="i" or app.lt=="em":
            app.elements.append(Label(data,app.x,app.y,italic=True,fill=app.textcolor))
            left()
        elif app.lt=="u":
            app.elements.append(Label(data,app.x,app.y,fill=app.textcolor))
            left()
            app.elements.append(Line(app.elements[-1].left,app.y+5,app.elements[-1].right,app.y+5,lineWidth=1))
        elif app.lt=="a":
            if app.textcolor=="white":
                tmp="cyan"
            else:
                tmp="blue"
            app.elements.append(Label(data,app.x,app.y,fill=tmp))
            app.elements[-1].url=app.attrs[-1][-1]
            app.elements[-1].type="hyperlink"
            left()
            app.elements.append(Line(app.elements[-1].left,app.y+5,app.elements[-1].right,app.y+5,fill=tmp,lineWidth=1))
        elif app.lt=="strong":
            app.elements.append(Label(data,app.x,app.y,bold=True,fill=app.textcolor))
            left()
        elif app.lt=="ul":
            app.y+=20
            app.elements.append(Label(data,app.x+20,app.y,fill=app.textcolor))
            app.elements[-1].left=30
            app.y+=20
            app.indented=True
        elif app.lt=="li":
            app.elements.append(Circle(app.x-10,app.y+1,3))
            left()
            app.elements.append(Label(data,app.x-10,app.y,fill=app.textcolor))
            app.elements[-1].left=app.elements[-2].right+20
            app.y+=20
        elif app.lt=="img":
            for i in range(len(app.attrs)):
                if app.attrs[i][0]=="src":
                    src=app.attrs[i][1]
            if src==app.lastimg:
                app.lastimg=src
            else:
                if not os.path.exists(data):
                    for i in range(len(app.attrs)):
                        if app.attrs[i][0]=="src":
                            src=app.attrs[i][1]
                    if src.startswith("http"):
                        try:
                            app.elements.append(Image(src,app.x-10,app.y))
                            app.lastimg=src
                        except:
                            pass
                    else:
                        try:
                            if not args.url.endswith(".htm") and not args.url.endswith(".html"):
                                print(args.url+"/"+src)
                                app.elements.append(Image(args.url+"/"+src,app.x-10,app.y))
                            else:
                                app.elements.append(Image(os.path.dirname(args.url)+"/"+src,app.x-10,app.y))
                            app.lastimg=src
                        except Exception as e:
                            print(e)
                            app.elements.append(Image("https://cdn.jsdelivr.net/gh/Stinkalistic/SwagBrowser/missing.png",app.x-10,app.y))
                else:
                    app.elements.append(Image(data,app.x-10,app.y))
                    app.lastimg=src
                app.y+=(app.elements[-1].bottom-app.elements[-1].top)+10            
        elif app.lt=="title":
            print(data)
            title=data
        elif app.lt=="color":
            app.background=data
        elif app.lt=="button":
            temp=Label(data,app.x,app.y)
            if app.textcolor!="white":
                app.elements.append(Group(Rect(temp.left-5,temp.top-5,temp.right+5-temp.left+5,22,fill="lightGrey",border="black"),Label(data,app.x,app.y,fill=app.textcolor)))
            else:
                app.elements.append(Group(Rect(temp.left-5,temp.top-5,temp.right+5-temp.left+5,22,fill="grey",border="black"),Label(data,app.x,app.y,fill=app.textcolor)))
            left()
            temp.visible=False
        elif app.lt=="source":
            for i in range(len(app.attrs)):
                if app.attrs[i][0]=="src":
                    src=app.attrs[i][1]
            if src==app.lastsnd:
                app.lastsnd=src
            else:
                print(src)
                temp=Label(os.path.basename(src),app.x,app.y)
                app.elements.append(Group(Rect(temp.left-5,temp.top-5,temp.right+5-temp.left+5,22,fill="lightGrey",border="black"),Label(os.path.basename(src),app.x,app.y)))
                left()
                temp.visible=False
                if src.startswith("http"):
                    app.elements[-1].sound=Sound(src)
                else:
                    if args.url.endswith(".html") or args.url.endswith(".htm"):
                        app.elements[-1].sound=Sound((os.path.dirname(args.url)+"/"+src))
                    else:
                        app.elements[-1].sound=Sound((args.url+src))
                app.lastsnd=src
        
        if app.y>app.yold:
            app.yold=app.y
            app.x=20




parser=MyHTMLParser()

if not args.input:
    i=input("enter html or name of file: \n")
else:
    i=args.input
try:
    with open(i,"r") as f:
        lines=f.readlines()
        for j in range(len(lines)):
            parser.feed(lines[j])
except:
    parser.feed(i)

def onMousePress(x,y):
    for element in app.elements:
        if element.contains(x,y):
            try:
                element.url
                if element.type=="hyperlink":
                    element.fill="purple"
                    app.elements[app.elements.index(element)+1].fill="purple"
                    print("opening URL "+element.url)
                    if linkopener:
                        if element.url.startswith("http"):
                            try:
                                subprocess.run("py browser.py -u "+element.url)
                            except:
                                subprocess.run("python browser.py -u "+element.url)
                        elif os.path.basename(element.url).endswith(".htm") or "/" in os.path.basename(element.url) or not "." in os.path.basename(element.url) or os.path.basename(element.url).endswith(".html"):
                            if args.url.endswith(".htm") or args.url.endswith(".html"):
                                try:
                                    subprocess.run("py browser.py -u "+os.path.dirname(args.url)+"/"+element.url)
                                except:
                                    subprocess.run("python browser.py -u "+os.path.dirname(args.url)+"/"+element.url)
                            else:
                                try:
                                    subprocess.run("py browser.py -u "+args.url+"/"+element.url)
                                except:
                                    subprocess.run("py browser.py -u "+args.url+"/"+element.url)
                        elif "." in os.path.basename(element.url):
                            print("downloading ",element.url)
                            if not args.url.endswith(".html") and not args.url.endswith(".htm"):
                                subprocess.run("curl "+args.url+"/"+element.url+" -O -L")
                            else:
                                subprocess.run("curl "+os.path.dirname(args.url)+"/"+element.url+" -O -L")
                    else:
                        web.open(element.url)
                    
            except:
                try:
                    element.sound.play()
                except:
                    pass
def onKeyHold(keys):
    if "down" in keys:
        for element in app.elements:
            element.centerY-=app.scrollspeed
    if "up" in keys:
        for element in app.elements:
            element.centerY+=app.scrollspeed
    if "right" in keys:
        for element in app.elements:
            element.centerX-=app.scrollspeed
    if "left" in keys:
        for element in app.elements:
            element.centerX+=app.scrollspeed
            
def onKeyPress(key):
    global title
    if key=="b" and args.url:
        if os.path.exists("bookmarks.txt"):
            mode="a"
        else:
            mode="w"
        with open("bookmarks.txt",mode) as file:
            if title.isspace():
               title=args.url.removeprefix("https://").removeprefix("http://")
            file.write((args.url+"||"+title+"\n"))
            print(f"{args.url} saved to bookmarks")
    
cmu_graphics.run()