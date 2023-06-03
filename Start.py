#!/usr/bin/env python3
import threading,time,os,random,json,sys,socket,subprocess,base64,requests,string,platform,pkg_resources
from concurrent.futures import ThreadPoolExecutor
from colorama  import init, Fore, Back, Style
from itertools import repeat
from pkg_resources import DistributionNotFound, VersionConflict
from pathlib import Path
from time import time as timer

def TryPHP():
    try:
       subprocess.call(['php', '--version'], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    except:
        print(f"\n{Fore.RED}[x] {Fore.YELLOW}php is not installed and you need to install it\n")
        quit()

def pkg_install():
  if platform.system() == "Linux":
      import apt
      cache = apt.cache.Cache()
      cache.update()
      cache.open()
      for pkg_name in ["php","python3-pip","php-curl"]:
        pkg = cache[pkg_name]
        if pkg.is_installed:
            pass  
        else:
            pkg.mark_install()
            try:
                cache.commit()
            except:
                print("Sorry, package installation failed")  

  for requirement in ['colorama','requests']:
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, VersionConflict):
        try:
           subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
           clear() 
        except:
           pass        
        
def convert(seconds):
  min, sec = divmod(seconds, 60)
  hour, min = divmod(min, 60)
  return "%d Hours, %2d Minutes and Seconds %02d" % (hour, min, sec)

def close(message):
    global pool
    global worker
    worker = False
    print(f"\n{Fore.RED}[x] {Fore.YELLOW}{message}")
    pool.close()
    pool.terminate()
    quit()

def fortnite(email,smtp,value,daba,state):
    global success 
    global error 
    global total_smtp
    if state:
        success+=1
        color=Fore.GREEN
    else:
        color=Fore.RED
        if "SMTP Error The following recipients failed" not in  value:
          error+=1
        #if smtp not in azzouz:
          #error+=1
          #azzouz.append(smtp)
            
    HOST = smtp.split('|')[2].split('@')[1]+":"+smtp.split('|')[1]
    print(f"{Fore.YELLOW}[{Fore.CYAN}{daba}{Fore.YELLOW}/{Fore.CYAN}{total_email}{Fore.YELLOW}] {email} {Fore.CYAN}| {Fore.YELLOW}{HOST} {Fore.CYAN}| {color}{value}")
    if platform.system() == "Windows":
        try:
            os.system(f"title Available SMTP:[{total_smtp-error}]     Error SMTP:[{error}]     Pending Mail:[{total_email-success}]     Sent Mail:[{success}]")
        except:pass

    
def echo(response,smtp,email):
    global success 
    global error 
    global bad 
    global current
    current+=1  
    value = response["Message"]
    
    if response["Exit"] == True:
        close(value)
    elif response["Status"] == True:
        success+=1
        color=Fore.GREEN
    else:
       if value=="Message sent but not received":
         bad+=1
         color=Fore.LIGHTYELLOW_EX
       else:
         error+=1
         color=Fore.RED                
    pending=count-success+error+bad    
    HOST = smtp.split('|')[2].split('@')[1]+":"+smtp.split('|')[1]
    print(f"{Fore.YELLOW}[{Fore.CYAN}{current}{Fore.YELLOW}/{Fore.CYAN}{count}{Fore.YELLOW}] {Fore.YELLOW}{HOST} {Fore.CYAN}| {Fore.MAGENTA}{email} {Fore.CYAN}| {color}{value}")
    if platform.system() == "Windows":
        try:
            os.system(f"title Pending SMTP:[{pending}]     Success SMTP:[{success}]     Error SMTP:[{error}]     Bad SMTP:[{bad}]")
        except:pass
    
def Start(file,data,test,email):
  global key
  global event
  global dragon
  global worker
  global currents
  global logs
  if worker == True:
      
      filename = "file/Smtps/"+data['Files']['Smtp']  
      all = open(filename,'r').read().split('\n')
      total = len(all)
      if os.path.getsize(filename) == 0:
          close("SMTP not found in your list")
      if data['Settings']['Loopsmtp'] == "random":
          smtp = random.choice(all)
      else:
          if total == key:
            key=0
          smtp = all[key] 
          key+=1
      if data['Activated']['Sleep'] == True:
         if event == int(data['Settings']['After']):
           time.sleep(int(data['Settings']['Sleep']))
           event=0
         event+=1 

      if data['Activated']['Delivery'] == True:     
          if smtp in dragon:
            dragon[smtp]+= 1
          else:
            dragon[smtp]= 1
          if dragon[smtp] == data['Settings']['Number']:
              dragon[smtp]= 0
              encode = base64.b64encode(smtp.encode("ascii")).decode("ascii")
              process,stderr = subprocess.Popen(['php', 'includes/Sender.php',file,encode,test,logs], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate() 
              response = json.loads(process)
              value = response["Message"]      
              if response["Exit"] == True:
                 close(value)
              elif response["Status"] == True:
                 fortnite(email,smtp,value,currents,True)
              else:
                 fortnite(email,smtp,value,currents,False)
                 key-=1
                 return Start(file,data,test,test)                 
      encode = base64.b64encode(smtp.encode("ascii")).decode("ascii")
      process,stderr = subprocess.Popen(['php', 'includes/Sender.php',file,encode,email,logs], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate() 
      response = json.loads(process)
      value = response["Message"]      
      if response["Exit"] == True:
         close(value)
      elif response["Status"] == True:
         fortnite(email,smtp,value,currents,True)
      else:
         fortnite(email,smtp,value,currents,False)
         if "SMTP Error The following recipients failed" not in  value:
           key-=1
           return Start(file,data,test,email)
      currents+=1    
def Sender():
         global total_smtp
         global total_email
         global logs

         number=0
         retxed = os.listdir("configuration")
         if not len(retxed):
            print(f"\n{Fore.RED}[x] {Fore.YELLOW}Files not found, you need to create a new configuration file")
            time.sleep(3) 
            return(home())
         print("")
         for dexter in retxed:
           number+=1
           print(f"{Fore.CYAN} [{number}]: {Fore.MAGENTA}{dexter}")
         select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
         select = select-1  
         file = retxed[select]
         test = json.loads(open("Settings.json", "r").read())["Mail"]["email"]
         data = json.loads(open(f"configuration/{file}", "r").read())
         
         Emails = open(Exsist("file/Maillist/"+data['Files']['Maillist']),'r').read().split('\n')
         Smtps = open(Exsist("file/Smtps/"+data['Files']['Smtp']),'r').read().split('\n') 
         if os.path.getsize("file/Maillist/"+data['Files']['Maillist']) == 0:
           print(f"\n{Fore.RED}[x] {Fore.YELLOW}Emails not found in your list")
           quit()
         elif os.path.getsize("file/Smtps/"+data['Files']['Smtp']) == 0:
           print(f"\n{Fore.RED}[x] {Fore.YELLOW}SMTP not found in your list")
           quit()
         print(f"\n{Fore.YELLOW}[Config]: {Fore.RED}{file}\n") 
         print(f"{Fore.YELLOW}[Name]: {Fore.RED}{data['Sender']['Name']}") 
         print(f"{Fore.YELLOW}[Subject]: {Fore.RED}{data['Sender']['Subject']}") 
         print(f"{Fore.YELLOW}[Email]: {Fore.RED}{data['Sender']['Email']}") 
         if data['Activated']['Delivery'] == True: check_token(data)
         total_smtp=len(Smtps)
         total_email=len(Emails)
         print(f"\n{Fore.YELLOW}[Total Smtp]: {Fore.RED}{total_smtp}") 
         print(f"{Fore.YELLOW}[Total Mail]: {Fore.RED}{total_email}") 
         thread = int(input(f"\n{Fore.YELLOW}[Thread]: {Fore.WHITE}"))
         print(f"\n{Fore.YELLOW}[Clear old history data]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
         history = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
         if history == 1:
           Remove_history(1)
         elif history == 2:
           pass
         else:
           print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
           quit()   
         print(f"\n{Fore.YELLOW}[Saving Logs]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
         save = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
         if save == 1:
           logs = "True"          
           if platform.system() == "Windows":os.system("Statistics.html");
         elif save == 2:
           logs = "False"
         else:
           print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
           quit()                
         print("")
         start= timer()
         with ThreadPoolExecutor(thread) as pool:
            pool.map(Start, repeat(file),repeat(data),repeat(test), Emails)        
         print('\nTime: ',convert(timer()-start),"\n\n") 
         
def check_token(data):
    zabi = json.loads(open("Settings.json", "r").read())
    response = requests.get('https://api.mail.tm/me', headers={"Authorization": f"Bearer {zabi['Mail']['auth']}"})
    student = json.loads(response.text)
    if "code" in student:
     print(f"\n{Fore.RED}[x] {Fore.YELLOW}{student['message']} Settings.json")
     quit()
    else:
     print(f"\n{Fore.YELLOW}[Test]: {Fore.CYAN}{zabi['Mail']['email']}\n")
     print(f"{Fore.YELLOW}[Delivery] Check after sending {Fore.RED}{data['Settings']['Number']} {Fore.YELLOW}email for every smtp If it is not delivered will be: {Fore.RED}{data['Settings']['Smtp']}")

def Exsist(file):
  if Path(file).is_file():
    return(file)
  else:
    print(f'\nThe file {file} does not exist\n')
    quit() 

def Remove_history(type):
 if type==1:
    files = ["output/Sender/connect_failed.txt", "output/Sender/sent_success.txt", "output/Sender/bad_delivery.txt", "output/Sender/data.js"]
    for file in files:
      f = open(file, "w+")
      f.close() 
    f = open("output/Sender/data.js", "w")
    f.write('var dataSet = { "Statics": [], "Sender": [], "Info": { "Failed": 0, "Available": 0, "Error": 0, "Pending": 0, "Sent": 0 }, "Link": { "Available": "#", "Pending": "#" } }')
    f.close() 
 elif type==2:
    files = ["output/Validate/connect_failed.txt", "output/Validate/bad_delivery.txt"]
    for file in files:
      f = open(file, "w+")
      f.close() 
    
def String():
  str = random.choice(string.ascii_letters).lower()
  if Path(f"file/Maillist/{str}_1.txt").is_file():
     return(String())
  else:
     return(str)
     
def split_emails():
            filename = scandir("file/Maillist")  
            digit = String()
            with open(Exsist(f"file/Maillist/{filename}")) as file:
                content = file.read().splitlines()
            count = input(f'\n{Fore.YELLOW}[•] How many lines per file: {Fore.WHITE}')
            c = 0
            i = 1
            for item in content:
                if c == int(count):
                    c = 0
                    i += 1
                    nline = '\n'
                elif item == content[-1]:
                    nline = ''
                else:
                    nline = '\n'
                with open(f'file/Maillist/{digit}_{i}.txt', 'a+') as file:
                    file.write(f'{item}{nline}')
                c += 1
            print(f'\n{Fore.RED}[•] {Fore.GREEN}{len(content)} {Fore.YELLOW}has been divided into {Fore.GREEN}{i} {Fore.YELLOW}files.')
            print(f'\n{Fore.RED}[•] {Fore.YELLOW}Check {Fore.GREEN}"Maillist" {Fore.YELLOW}Folder')

  
def duplicates():
    zab = scandir("file/Maillist") 
    get = open(Exsist(f"file/Maillist/{zab}"),'r').read().split('\n')
    print (f"\n{Fore.YELLOW}[Total]: {Fore.WHITE}",len(get))
    mylist = list(dict.fromkeys(get))
    open(f"file/Maillist/{zab}", 'w').write("\n".join(mylist))
    print (f"\n{Fore.RED}[Removed]: {Fore.WHITE}",len(get)-len(mylist))
    
    
def Remove():
         number=0
         data = ["configuration","Attachment","embed","Header","Letter","Maillist","RandomLink","Smtps"]
         print("\n")
         for file in data:
            number+=1
            print(f"{Fore.CYAN} [{number}]: {Fore.MAGENTA}{file}")
         back = number+1 
         print(f"{Fore.CYAN} [{back}]: {Fore.YELLOW}Back")   
         select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))   
         if back == select:
              return(home())         
         
         select = select-1
         folder = data[select]
         if folder == "configuration":
            pass
         else:
            folder = "file/"+folder  

         number=0
         data = os.listdir(folder)
         if not len(data):
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Files not found in directory {folder}")
              time.sleep(3) 
              clear()
              banner()
              return(Remove())     
         else:
              print("\n")
              for file in data:
                number+=1
                print(f"{Fore.CYAN} [{number}]: {Fore.MAGENTA}{file}")
              select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
              select = select-1
              
         dragoncrew =  data[select]
         if not len(dragoncrew):
            print(f"\n{Fore.RED}[x] {Fore.YELLOW}Files not found, you need to create a new configuration file")
            time.sleep(3) 
            return(home())         
         where = f"{folder}/{dragoncrew}"
         if os.path.exists(where):
            os.remove(where)
            print(f"\n{Fore.RED}[x] {Fore.YELLOW}File removed successfully {dragoncrew}")
         else:
            print(f"\n{Fore.RED}[x] {Fore.YELLOW}The file does not exist")
 
         time.sleep(3)
         clear()
         banner()           
         return(Remove())

def View():
         ppp=0
         mm = os.listdir("configuration")
         if not len(mm):
            print(f"\n{Fore.RED}[x] {Fore.YELLOW}Files not found, you need to create a new configuration file")
            time.sleep(3) 
            return(home())
         print("\n")
         for file in mm:
           ppp+=1
           print(f"{Fore.CYAN} [{ppp}]: {Fore.MAGENTA}{file}")
         select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
         select = select-1  
         dragoncrew= mm[select]
         readme = open(f"configuration/{dragoncrew}", "r")
         print(f"\n{Fore.YELLOW}[Files]: {Fore.RED}{dragoncrew}") 
         data = json.loads(readme.read())
         print("\n")
 

         print(f"\n{Fore.MAGENTA}[Activated]\n")   
         
         for key in data["Activated"]:
            if key == "Email":pass
            elif key == "Name":pass           
            elif key == "Subject":pass  
            else:            
                if data["Activated"][key] == True:
                 zab = Fore.GREEN
                else:
                 zab = Fore.RED
                print(f"{Fore.CYAN}[{key.capitalize()}] {zab}{data['Activated'][key]}")
                
         print(f"\n{Fore.MAGENTA}[Sender]\n")   
               
         for key in data["Sender"]:
            print(f"{Fore.CYAN}[{key.capitalize()}] {Fore.YELLOW}{data['Sender'][key]}")

         print(f"\n{Fore.MAGENTA}[Files]\n")   

         for key in data["Files"]:
            print(f"{Fore.CYAN}[{key.capitalize()}] {Fore.YELLOW}{data['Files'][key]}")

         print(f"\n{Fore.MAGENTA}[Settings]\n")   

         for key in data["Settings"]:
           if "After" == key:
            print(f"{Fore.CYAN}[Delivery] {Fore.YELLOW}Check send after sending the number {Fore.RED}{data['Settings']['Number']} {Fore.YELLOW}If it is not delivered will be: {Fore.RED}{data['Settings']['Smtp']}")
           if "Sleep" == key:
            print(f"{Fore.CYAN}[Sleep] {Fore.YELLOW}Time {Fore.RED}{data['Settings']['Sleep']} {Fore.YELLOW}secound after number {Fore.RED}{data['Settings']['After']}")
           if "Loopsmtp" == key:
            print(f"{Fore.CYAN}[Loops] {Fore.YELLOW}{data['Settings']['Loopsmtp'].capitalize()}")

       
         input(f"\n{Fore.YELLOW}[Press enter to return]{Fore.WHITE}")   
         return(home())

def Editor(dragoncrew,check=False):
         ppp=0
         mm = os.listdir("configuration")
         if not len(mm):
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Files not found, you need to create a new configuration file")
          time.sleep(3) 
          return(home())
         
         print("\n")
         if check==False:
             for file in mm:
               ppp+=1
               print(f"{Fore.CYAN} [{ppp}]: {Fore.MAGENTA}{file}")
             select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
             select = select-1  
             dragoncrew= mm[select]
             readme = open(f"configuration/{dragoncrew}", "r")
         else:
             readme = open(f"configuration/{dragoncrew}", "r")
         print(f"\n{Fore.YELLOW}[Files]: {Fore.RED}{dragoncrew}") 
         data = json.loads(readme.read())
         dexter=0
         test=0
         print("\n")
         for key in data["Activated"]:
            if data["Activated"][key] == True:
             zab = Fore.GREEN
            else:
             zab = Fore.RED
            dexter+=1    
            print(f"{Fore.CYAN}[{dexter}] {zab}{key.capitalize()}")
         back = dexter+1 
         print(f"{Fore.CYAN}[{back}] {Fore.YELLOW}Back")   
         select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))   
         
         if back == select:
              return(home())
         else:
             for key in data["Activated"]:
                test+=1
                if test == select: 
                   value = key        
                   break
             try:
             
               number = value
               
             except:
               print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
               quit()

         if "Email" == number:
            print(f"\n{Fore.YELLOW}[Email]: {Fore.YELLOW}{data['Sender']['Email']}") 
            fromemail = format(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}")) 
            data['Sender']["Email"] = fromemail
         elif "Name" == number:
            print(f"\n{Fore.YELLOW}[Name]: {Fore.YELLOW}{data['Sender']['Name']}") 
            fromname = format(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}")) 
            data['Sender']["Name"] = fromname 
         elif "Subject" == number:
            print(f"\n{Fore.YELLOW}[Subject]: {Fore.YELLOW}{data['Sender']['Subject']}") 
            subject = format(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}")) 
            data['Sender']["Subject"] = subject 
         elif "Letter" == number:
            print(f"\n{Fore.YELLOW}[Letter]: {Fore.YELLOW}{data['Files']['Letter']}")
            Letterfile = scandirnew("file/Letter")
            data['Files']["Letter"] = Letterfile            
         elif "Maillist" == number:
            print(f"\n{Fore.YELLOW}[Maillist]: {Fore.YELLOW}{data['Files']['Maillist']}")
            emails = scandirnew("file/Maillist")
            data['Files']["Maillist"] = emails
         elif "Replyto" == number:
            print(f"\n{Fore.YELLOW}[Reply-to]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
              Replyto= True
              if data['Activated']["Replyto"]:print(f"\n{Fore.YELLOW}[Reply-to]: {Fore.YELLOW}{data['Sender']['Replyto']}")
              else:print(f"\n{Fore.YELLOW}[Reply-to]")
              to = format(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
            elif number == 2:
              Replyto= False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()     
            data['Activated']["Replyto"] = Replyto    
            data['Sender']["Replyto"] = to 
         elif "Attachment" == number:
            print(f"\n{Fore.YELLOW}[Attachment]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
              Attachment = True
              if data['Activated']["Attachment"]: print(f"\n{Fore.YELLOW}[File]: {Fore.YELLOW}{data['Files']['Attachfile']}")
              else: print(f"\n{Fore.YELLOW}[File]")
              Attachfile = scandirnew("file/Attachment")
              data['Files']["Attachfile"] = Attachfile
              print(f"\n{Fore.YELLOW}[File Type]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Default\n{Fore.CYAN} [2]: {Fore.RED}Change")
              retxed = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}")) 
              if retxed == 1: 
                 filename = os.path.basename(Attachfile)
                 data['Files']["Attachname"] = filename
              elif retxed == 2:
                 print(f"\n{Fore.YELLOW}[File Name]: {Fore.YELLOW}{data['Files']['Attachfile']}")              
                 filename = format(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
                 data['Files']["Attachname"] = filename
              else:
                print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
                quit()  
              
              
            elif number == 2:
              Attachment = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()
       
            data['Activated']["Attachment"] = Attachment 
         elif "RandomLink" == number:
            print(f"\n{Fore.YELLOW}[RandomLink]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
              RandomLink = True
              if data['Activated']["RandomLink"]:print(f"\n{Fore.YELLOW}[File]: {Fore.YELLOW}{data['Files']['RandomLink']}")
              else:print(f"\n{Fore.YELLOW}[File]")
              Randomfile = scandirnew("file/RandomLink")
              data['Files']["RandomLink"] = Randomfile
            elif number == 2:
              RandomLink = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()  
            data['Activated']["RandomLink"] = RandomLink       
         elif "Headers" == number:
            print(f"\n{Fore.YELLOW}[CustomHeader]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
              Header = True
              if data['Activated']["Headers"]:print(f"\n{Fore.YELLOW}[File]: {Fore.YELLOW}{data['Files']['Header']}")
              else:print(f"\n{Fore.YELLOW}[File]")
              Headerfile = scandirnew("file/Header")
              data['Files']["Header"] = Headerfile
            elif number == 2:
              Header = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()   
            data['Activated']["Headers"] = Header 
         elif "NameEncode" == number:
            print(f"\n{Fore.YELLOW}[Name-Encode]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
               NameType = True
               if data['Activated']["NameEncode"]:print(f"\n{Fore.YELLOW}[Name-Encode]: {Fore.YELLOW}{data['Encoder']['NameEncode']}")
               else:print(f"\n{Fore.YELLOW}[Name-Encode]")
               print(f"\n{Fore.CYAN} [1]: {Fore.YELLOW}7bit\n{Fore.CYAN} [2]: {Fore.YELLOW}base64\n{Fore.CYAN} [3]: {Fore.YELLOW}binary\n{Fore.CYAN} [4]: {Fore.YELLOW}quoted-printable")
               Select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
               if Select == 1: 
                   NameEncode = "7bit"
                   data['Encoder']['NameEncode'] = NameEncode  
               elif Select == 2:
                   NameEncode = "base64"
                   data['Encoder']['NameEncode'] = NameEncode  
               elif Select == 3:
                   NameEncode = "binary"
                   data['Encoder']['NameEncode'] = NameEncode 
               elif Select == 4:
                   NameEncode = "quoted-printable"
                   data['Encoder']['NameEncode'] = NameEncode 
               else:
                  print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
                  quit() 
            elif number == 2:
              NameType = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()   
            data['Activated']["NameEncode"] = NameType     
         elif "SubjectEncode" == number:
            print(f"\n{Fore.YELLOW}[Subject-Encode]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
               SubjectType = True
               if data['Activated']["SubjectEncode"]:print(f"\n{Fore.YELLOW}[Subject-Encode]: {Fore.YELLOW}{data['Encoder']['SubjectEncode']}")
               else:print(f"\n{Fore.YELLOW}[Subject-Encode]")
               print(f"\n{Fore.CYAN} [1]: {Fore.YELLOW}7bit\n{Fore.CYAN} [2]: {Fore.YELLOW}base64\n{Fore.CYAN} [3]: {Fore.YELLOW}binary\n{Fore.CYAN} [4]: {Fore.YELLOW}quoted-printable")
               Select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
               if Select == 1: 
                   SubjectEncode = "7bit"
                   data['Encoder']["SubjectEncode"] = SubjectEncode
               elif Select == 2:
                   SubjectEncode = "base64"
                   data['Encoder']["SubjectEncode"] = SubjectEncode
               elif Select == 3:
                   SubjectEncode = "binary"
                   data['Encoder']["SubjectEncode"] = SubjectEncode
               elif Select == 4:
                   SubjectEncode = "quoted-printable"
                   data['Encoder']["SubjectEncode"] = SubjectEncode
               else:
                  print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
                  quit() 
            elif number == 2:
              SubjectType = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()                
            data['Activated']["SubjectEncode"] = SubjectType     
         elif "Charset" == number:
            
            print(f"\n{Fore.YELLOW}[Charset]: {data['Encoder']['Charset']}\n\n{Fore.CYAN} [1]: {Fore.YELLOW}UTF-8\n{Fore.CYAN} [2]: {Fore.YELLOW}US-ASCII\n{Fore.CYAN} [3]: {Fore.YELLOW}ISO-8859-1")
            number = int(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
            if number == 1:
               charset = "UTF-8"
               data['Encoder']["Charset"] = charset   
            elif number == 2:
               charset = "US-ASCII"
               data['Encoder']["Charset"] = charset   
            elif number == 3:
               charset = "ISO-8859-1" 
               data['Encoder']["Charset"] = charset           
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()            
            data['Activated']["Charset"] = True      
         elif "LetterEncode" == number:
            print(f"\n{Fore.YELLOW}[Letter-Encoding]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
               encodemsg = True
               if data['Activated']["LetterEncode"]:print(f"\n{Fore.YELLOW}[Letter-Encoding]: {Fore.YELLOW}{data['Encoder']['Encoding']}")
               print(f"\n{Fore.CYAN} [1]: {Fore.YELLOW}7bit\n{Fore.CYAN} [2]: {Fore.YELLOW}8bit\n{Fore.CYAN} [3]: {Fore.YELLOW}base64\n{Fore.CYAN} [4]: {Fore.YELLOW}binary\n{Fore.CYAN} [5]: {Fore.YELLOW}quoted-printable")
               Select = int(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
               if Select == 1: 
                   content = "7bit"
                   data['Encoder']["Encoding"] = content
               elif Select == 2:
                   content = "8bit"
                   data['Encoder']["Encoding"] = content
               elif Select == 3:
                   content = "base64"
                   data['Encoder']["Encoding"] = content
               elif Select == 4:
                   content = "binary"
                   data['Encoder']["Encoding"] = content
               elif Select == 5:
                   content = "quoted-printable"
                   data['Encoder']["Encoding"] = content
               else:
                  print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
                  quit()  
            elif number == 2:
               encodemsg = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()  
            data['Activated']["LetterEncode"] = encodemsg      
         elif "Priority" == number:
            print(f"\n{Fore.YELLOW}[Priority]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
               Priority = True
               if data['Activated']["Priority"]:print(f"\n{Fore.YELLOW}[Priority]: {Fore.YELLOW}{data['Encoder']['Priority']}")
               else:print(f"\n{Fore.YELLOW}[Priority]")
               print(f"\n{Fore.CYAN} [1]: {Fore.YELLOW}Low\n{Fore.CYAN} [2]: {Fore.YELLOW}Normal\n{Fore.CYAN} [3]: {Fore.YELLOW}High\n{Fore.CYAN}")
               Select = int(input(f"{Fore.YELLOW}[New]: {Fore.WHITE}"))
               if Select == 1: 
                   Prioritycode = "Low"
                   data['Encoder']["Priority"] = Prioritycode 
               elif Select == 2:
                   Prioritycode = "Normal"
                   data['Encoder']["Priority"] = Prioritycode 
               elif Select == 3:
                   Prioritycode = "High"
                   data['Encoder']["Priority"] = Prioritycode   
               else:
                  print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
                  quit()  
            elif number == 2:
               Priority = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit() 
            data['Activated']["Priority"] = Priority                   
         elif "Boundary" == number:
            if data['Activated']["Boundary"] == 1:
              print(f"\n{Fore.YELLOW}[Boundary]: {Fore.YELLOW}{Fore.GREEN}Yes")
            else:
              print(f"\n{Fore.YELLOW}[Boundary]: {Fore.YELLOW}{Fore.RED}No")
            print(f"\n{Fore.YELLOW}[Boundary]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
            if number == 1:
              Boundary = True
            elif number == 2:
              Boundary = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()            
            data['Activated']["Boundary"] = Boundary
         elif "Bounce" == number:
            print(f"\n{Fore.YELLOW}[Return Patch Bounce]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
              Bounce_Type = True
              if data['Activated']["Bounce"]:
                print(f"\n{Fore.YELLOW}[Email]: {Fore.YELLOW}{data['Bounce']}")
                Bounce_email = format(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
              else:
                Bounce_email = format(input(f"\n{Fore.YELLOW}[Email]: {Fore.WHITE}"))
              data['Bounce'] = Bounce_email 
            elif number == 2:
              Bounce_Type = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()  
            data['Activated']["Bounce"] = Bounce_Type     
         elif "Smtp" == number:      
            print(f"\n{Fore.YELLOW}[Smtps]: {Fore.YELLOW}{data['Files']['Smtp']}")
            smtps = scandirnew("file/Smtps")
            data['Files']["Smtp"] = smtps
            print(f"\n{Fore.YELLOW}[Loop Lists SMTP]: {Fore.YELLOW}{data['Settings']['Loopsmtp']}")
            print(f"\n{Fore.YELLOW}[Loop Lists SMTP]\n\n{Fore.CYAN} [1]: {Fore.YELLOW}Random\n{Fore.CYAN} [2]: {Fore.YELLOW}For one by one")
            number = int(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
            if number == 1:
               loops = "random"
               data['Settings']['Loopsmtp'] = loops
            elif number == 2:
               loops = "for"
               data['Settings']['Loopsmtp'] = loops
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()           
         elif "Sleep" == number:
            print(f"\n{Fore.YELLOW}[Sleep Send]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
              Sleep = True
              if data['Activated']["Sleep"]:print(f"\n{Fore.YELLOW}[Sleep Second]: {Fore.YELLOW}{data['Settings']['Sleep']}") 
              else:print(f"\n{Fore.YELLOW}[Sleep Second]") 
              sleepsend = int(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
              data['Settings']["Sleep"] = sleepsend  
              if data['Activated']["Sleep"]:print(f"\n{Fore.YELLOW}[After Number]: {Fore.YELLOW}{data['Settings']['After']}") 
              else:print(f"\n{Fore.YELLOW}[After Number]")
              aftersend = int(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
              data['Settings']["After"] = aftersend  
            elif number == 2:
              Sleep = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()        
            data['Activated']["Sleep"] = Sleep  
         elif "Delivery" == number:
            print(f"\n{Fore.YELLOW}[Check email delivery]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
            number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
            if number == 1:
               delivery = True
               if data['Activated']["Delivery"]:print(f"\n{Fore.YELLOW}[After sending the number]: {Fore.YELLOW}{data['Settings']['Number']}") 
               else:print(f"\n{Fore.YELLOW}[After sending the number]") 
               numbersend = int(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
               data['Settings']["Number"] = numbersend 
               if data['Activated']["Delivery"]:print(f"\n {Fore.LIGHTYELLOW_EX}[If it is not delivered will be]\n\n  {Fore.YELLOW}[Old]: {Fore.YELLOW}{data['Settings']['Smtp']} \n\n{Fore.CYAN}   [1]: {Fore.YELLOW}Change SMTP\n{Fore.CYAN}   [2]: {Fore.YELLOW}Keep SMTP")
               else:print(f"\n {Fore.LIGHTYELLOW_EX}[If it is not delivered will be]\n\n{Fore.CYAN}   [1]: {Fore.YELLOW}Change SMTP\n{Fore.CYAN}   [2]: {Fore.YELLOW}Keep SMTP")
               Select = int(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
               if Select == 1: 
                   rotina = "Change"
                   data['Settings']["Smtp"] = rotina  
               elif Select == 2:
                   rotina = "Keep"
                   data['Settings']["Smtp"] = rotina  
               else:
                  print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
                  quit()              

            elif number == 2:
              delivery = False
            else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()  
            data['Activated']["Delivery"] = delivery     

         f = open(f"configuration/{dragoncrew}", "w")
         f.write(json.dumps(data, indent=4))
         f.close()
         print(f"\n{Fore.GREEN}[Success]: {Fore.YELLOW}Success file updated at {Fore.RED}{dragoncrew}")
         time.sleep(3) 
         clear()
         banner()
         return(Editor(dragoncrew,check=True))

def Create():
        data = {} 
        data['Encoder'] = {}  
        fromemail = format(input(f"\n{Fore.YELLOW}[Email]: {Fore.WHITE}")) 
        data['Activated'] = {"Email": True} 
        fromname = format(input(f"\n{Fore.YELLOW}[Name]: {Fore.WHITE}"))
        data['Activated']["Name"] = True  
        subject = format(input(f"\n{Fore.YELLOW}[Subject]: {Fore.WHITE}"))
        data['Activated']["Subject"] = True  
        data['Sender'] = {"Name": fromname,"Subject": subject,"Email": fromemail}
        clear()
        banner()
        print(f"\n{Fore.YELLOW}[Letter]")
        Letterfile = scandir("file/Letter")
        data['Files'] = {"Letter": Letterfile}
        data['Activated']["Letter"] = True
        clear()
        banner()
        print(f"\n{Fore.YELLOW}[Emails]")
        emails = scandir("file/Maillist")
        data['Files']["Maillist"] = emails
        data['Activated']["Maillist"] = True
        clear()
        banner()
        print(f"\n{Fore.YELLOW}[Reply-to]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        
        if number == 1:
          Replyto= True
          to = format(input(f"\n{Fore.YELLOW}[Reply-to]: {Fore.WHITE}"))
          data['Sender']["Replyto"] = to  
        elif number == 2:
          Replyto= False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit() 
        
        data['Activated']["Replyto"] = Replyto    
        
        clear() 
        banner()        
        print(f"\n{Fore.YELLOW}[Attachment]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
          Attachment = True
          Attachfile = scandir("file/Attachment")
          data['Files']["Attachfile"] = Attachfile
          print(f"\n{Fore.YELLOW}[File Name]\n\n{Fore.CYAN} [1]: {Fore.GREEN}default\n{Fore.CYAN} [2]: {Fore.RED}Change")
          retxed = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}")) 
          if retxed == 1: 
             filename = os.path.basename(Attachfile)
             data['Files']["Attachname"] = filename
          elif retxed == 2:    
             filename = format(input(f"\n{Fore.YELLOW}[Enter]: {Fore.WHITE}"))
             data['Files']["Attachname"] = filename
          else:
            print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
            quit() 
 
        elif number == 2:
          Attachment = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()
   
        data['Activated']["Attachment"] = Attachment        
        clear() 
        banner()
        print(f"\n{Fore.YELLOW}[RandomLink]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
          RandomLink = True
          Randomfile = scandir("file/RandomLink")
          data['Files']["RandomLink"] = Randomfile
        elif number == 2:
          RandomLink = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()  
        data['Activated']["RandomLink"] = RandomLink        
        clear()
        banner()
        print(f"\n{Fore.YELLOW}[CustomHeader]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
          Header = True
          Headerfile = scandir("file/Header")
          data['Files']["Header"] = Headerfile
        elif number == 2:
          Header = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()   
        data['Activated']["Headers"] = Header        
        clear()
        banner() 
        print(f"\n{Fore.YELLOW}[Name-Encode]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
           NameType = True
           print(f"\n{Fore.CYAN} [1]: {Fore.YELLOW}7bit\n{Fore.CYAN} [2]: {Fore.YELLOW}base64\n{Fore.CYAN} [3]: {Fore.YELLOW}binary\n{Fore.CYAN} [4]: {Fore.YELLOW}quoted-printable")
           Select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
           if Select == 1: 
               NameEncode = "7bit"
               data['Encoder']["NameEncode"] = NameEncode     
           elif Select == 2:
               NameEncode = "base64"
               data['Encoder']["NameEncode"] = NameEncode     
           elif Select == 3:
               NameEncode = "binary"
               data['Encoder']["NameEncode"] = NameEncode     
           elif Select == 4:
               NameEncode = "quoted-printable"
               data['Encoder']["NameEncode"] = NameEncode               
           else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit() 
        elif number == 2:
          NameType = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()   
        data['Activated']["NameEncode"] = NameType
        
        clear()
        banner()           
        print(f"\n{Fore.YELLOW}[Subject-Encode]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
           SubjectType = True
           print(f"\n{Fore.CYAN} [1]: {Fore.YELLOW}7bit\n{Fore.CYAN} [2]: {Fore.YELLOW}base64\n{Fore.CYAN} [3]: {Fore.YELLOW}binary\n{Fore.CYAN} [4]: {Fore.YELLOW}quoted-printable")
           Select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
           if Select == 1: 
               SubjectEncode = "7bit"
               data['Encoder']["SubjectEncode"] = SubjectEncode
           elif Select == 2:
               SubjectEncode = "base64"
               data['Encoder']["SubjectEncode"] = SubjectEncode
           elif Select == 3:
               SubjectEncode = "binary"
               data['Encoder']["SubjectEncode"] = SubjectEncode
           elif Select == 4:
               SubjectEncode = "quoted-printable"
               data['Encoder']["SubjectEncode"] = SubjectEncode
           else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit() 
        elif number == 2:
          SubjectType = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()                
        data['Activated']["SubjectEncode"] = SubjectType
        clear()
        banner()        
        print(f"\n{Fore.YELLOW}[Content-Type]\n\n{Fore.CYAN} [1]: {Fore.YELLOW}text/html\n{Fore.CYAN} [2]: {Fore.YELLOW}text/plain")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
           content = "text/html"
           data['Sender']["ContenType"] = content
        elif number == 2:
           content = "text/plain"
           data['Sender']["ContenType"] = content
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()    

        clear()
        banner()        
        print(f"\n{Fore.YELLOW}[Charset]\n\n{Fore.CYAN} [1]: {Fore.YELLOW}UTF-8\n{Fore.CYAN} [2]: {Fore.YELLOW}US-ASCII\n{Fore.CYAN} [3]: {Fore.YELLOW}ISO-8859-1")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
           charset = "UTF-8"
           data['Encoder']["Charset"] = charset   
        elif number == 2:
           charset = "US-ASCII"
           data['Encoder']["Charset"] = charset   
        elif number == 3:
           charset = "ISO-8859-1" 
           data['Encoder']["Charset"] = charset           
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()            
 
        data['Activated']["Charset"] = True 
        clear()
        banner()        
        print(f"\n{Fore.YELLOW}[Content-Encoding]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
           encodemsg = True
           print(f"\n{Fore.CYAN} [1]: {Fore.YELLOW}7bit\n{Fore.CYAN} [2]: {Fore.YELLOW}8bit\n{Fore.CYAN} [3]: {Fore.YELLOW}base64\n{Fore.CYAN} [4]: {Fore.YELLOW}binary\n{Fore.CYAN} [5]: {Fore.YELLOW}quoted-printable")
           Select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
           if Select == 1: 
               content = "7bit"
               data['Encoder']["Encoding"] = content
           elif Select == 2:
               content = "8bit"
               data['Encoder']["Encoding"] = content
           elif Select == 3:
               content = "base64"
               data['Encoder']["Encoding"] = content
           elif Select == 4:
               content = "binary"
               data['Encoder']["Encoding"] = content
           elif Select == 5:
               content = "quoted-printable"
               data['Encoder']["Encoding"] = content
           else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()  
        elif number == 2:
           encodemsg = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()  
        data['Activated']["LetterEncode"] = encodemsg   

        clear()
        banner()        
        print(f"\n{Fore.YELLOW}[Priority]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
           Priority = True
           print(f"\n{Fore.CYAN} [1]: {Fore.YELLOW}Low\n{Fore.CYAN} [2]: {Fore.YELLOW}Normal\n{Fore.CYAN} [3]: {Fore.YELLOW}High\n{Fore.CYAN}")
           Select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
           if Select == 1: 
               Prioritycode = "Low"
               data['Encoder']["Priority"] = Prioritycode 
           elif Select == 2:
               Prioritycode = "Normal"
               data['Encoder']["Priority"] = Prioritycode 
           elif Select == 3:
               Prioritycode = "High"
               data['Encoder']["Priority"] = Prioritycode   
           else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()  
        elif number == 2:
           Priority = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()            
        
        data['Activated']["Priority"] = Priority    
        clear()
        banner()
        print(f"\n{Fore.YELLOW}[Boundary]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
          Boundary = True
        elif number == 2:
          Boundary = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()            
        data['Activated']["Boundary"] = Boundary
        clear()
        banner()
        print(f"\n{Fore.YELLOW}[Return Patch Bounce]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
          Bounce_Type = True
          Bounce_email = format(input(f"\n{Fore.YELLOW}[Email]: {Fore.WHITE}"))
          data['Bounce'] = Bounce_email 
        elif number == 2:
          Bounce_Type = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()  
        data['Activated']["Bounce"] = Bounce_Type  
        clear()
        banner()
        
        
        
        print(f"\n{Fore.YELLOW}[Smtps]")
        smtps = scandir("file/Smtps")
        data['Files']["Smtp"] = smtps        
        data['Activated']["Smtp"] = True 
        
        print(f"\n{Fore.YELLOW}[Loop Lists SMTP]\n\n{Fore.CYAN} [1]: {Fore.YELLOW}Random\n{Fore.CYAN} [2]: {Fore.YELLOW}For one by one")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
           loops = "random"
           data['Settings'] = {"Loopsmtp": loops}
        elif number == 2:
           loops = "for"
           data['Settings'] = {"Loopsmtp": loops}
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()   
          
        print(f"\n{Fore.YELLOW}[Sleep Send]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
          Sleep = True
          sleepsend = int(input(f"\n{Fore.YELLOW}[Sleep Seconde]: {Fore.WHITE}"))
          data['Settings']["Sleep"] = sleepsend  
          aftersend = int(input(f"\n{Fore.YELLOW}[After Number]: {Fore.WHITE}"))
          data['Settings']["After"] = aftersend  
        elif number == 2:
          Sleep = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()             
  
        data['Activated']["Sleep"] = Sleep  
        print(f"\n{Fore.YELLOW}[Check email delivery]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
        number = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
        if number == 1:
           delivery = True
           numbersend = int(input(f"\n{Fore.YELLOW}[After sending the number]: {Fore.WHITE}"))
           data['Settings']["Number"] = numbersend 
           print(f"\n {Fore.LIGHTYELLOW_EX}[If it is not delivered will be] \n\n{Fore.CYAN}  [1]: {Fore.YELLOW}Change SMTP\n{Fore.CYAN}  [2]: {Fore.YELLOW}Keep SMTP")
           Select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
           if Select == 1: 
               rotina = "Change"
               data['Settings']["Smtp"] = rotina  
           elif Select == 2:
               rotina = "Keep"
               data['Settings']["Smtp"] = rotina  
           else:
              print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
              quit()              

        elif number == 2:
          delivery = False
        else:
          print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
          quit()  
          
        data['Activated']["Delivery"] = delivery  
 
        file = f"configuration/{lastfile('configuration')}.json"
        f = open(file, "a")
        f.write(json.dumps(data, indent=4))
        f.close()

        print(f"\n{Fore.GREEN}[Success]: {Fore.YELLOW}Success file registered at {file}\n\n")

        time.sleep(3) 
        return(home())
        
def scandir(folder):
  number=0
  data = os.listdir(folder)
  if not len(data):
      print(f"\n{Fore.RED}[x] {Fore.YELLOW}Files not found in directory {folder}")
      quit()
  else:
      print("")
      for file in data:
        number+=1
        print(f"{Fore.CYAN} [{number}]: {Fore.MAGENTA}{file}")
      select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
      select = select-1
      return(data[select])

def scandirnew(folder):
  number=0
  data = os.listdir(folder)
  if not len(data):
      print(f"\n{Fore.RED}[x] {Fore.YELLOW}Files not found in directory {folder}")
      quit()
  else:
      print("\n")
      for file in data:
        number+=1
        print(f"{Fore.CYAN} [{number}]: {Fore.MAGENTA}{file}")
      select = int(input(f"\n{Fore.YELLOW}[New]: {Fore.WHITE}"))
      select = select-1
      return(data[select]) 
 
def lastfile(folder):
 try:
   file = os.listdir(folder).pop()
   last = os.path.splitext(file)[0]
 except:
   last=0 
 return(int(last)+1)
 
def Starter(file,email,smtp):
  global worker
  if worker == True: 
      encode = base64.b64encode(smtp.encode("ascii")).decode("ascii")
      #process  = subprocess.run(['php', 'includes/Validate.php',encode,email,file], capture_output=True, text=True)
      process,stderr = subprocess.Popen(['php', 'includes/Validate.php',encode,email,file], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
      object = json.loads(process)
      echo(object,smtp,email)    
 
def Validate():

  global count
  file = scandir("file/Smtps")
  smtp = open(Exsist("file/Smtps/"+file),'r').read().split('\n')
  print(f"\n{Fore.YELLOW}[Check sent mail if delivered]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
  type = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
  if type == 1:
      zab = json.loads(open("Settings.json", "r").read())
      test = zab["Mail"]["email"]
      response = requests.get('https://api.mail.tm/me', headers={"Authorization": f"Bearer {zab['Mail']['auth']}"})
      student = json.loads(response.text)
      if "code" in student:
         print(f"\n{Fore.RED}[x] {Fore.YELLOW}{student['message']} Settings.json")
         quit()
      print(f"\n{Fore.YELLOW}[Email]: {Fore.CYAN}{test}")
      email = test
  elif type == 2:
      email = format(input(f"\n{Fore.YELLOW}[Email]: {Fore.WHITE}")) 
  else:
    print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
    quit()   
  count=len(smtp)
  print(f"\n{Fore.YELLOW}[Total Smtp]: {Fore.RED}{count}") 
  thread = int(input(f"\n{Fore.YELLOW}[Thread]: {Fore.WHITE}"))
  print(f"\n{Fore.YELLOW}[Clear old history data]\n\n{Fore.CYAN} [1]: {Fore.GREEN}Yes\n{Fore.CYAN} [2]: {Fore.RED}No")
  history = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
  print("")
  if history == 1:
    Remove_history(2)
  elif history == 2:
    pass
  else:
    print(f"\n{Fore.RED}[x] {Fore.YELLOW}Number is not exist")
    quit()
  if type == 1: 
    if platform.system() == "Windows":os.system("start https://mail.tm/en/")
  start= timer()  
  with ThreadPoolExecutor(thread) as pool:
     pool.map(Starter,repeat(file),repeat(email.replace(" ", "")), smtp)  
 
  print (f"\n{Fore.RED}[Removed]: {Fore.CYAN}{bad+error} {Fore.YELLOW}smtp Removed from the list {Fore.CYAN}file/Smtps/{file}")
  print('\nTime: ',convert(timer()-start),"\n\n")    
  
def Inbox(config,email,smtp):
  global error 
  global current
  global worker
  if worker == True:   
      current+=1   
      for file in config:
         for test in email:
            encode = base64.b64encode(smtp.encode("ascii")).decode("ascii")
            #process  = subprocess.run(['php', 'includes/Tester.php',file,encode,test], capture_output=True, text=True)
            #response = json.loads(process.stdout)
            process,stderr = subprocess.Popen(['php', 'includes/Tester.php',file,encode,test], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = json.loads(process)
            value = response["Message"]
            type=False
            if response["Exit"] == True:
                close(value)
            elif response["Status"] == True:
                color=Fore.GREEN
            else:
                error+=1
                color=Fore.RED
                type=True
                        
            HOST = smtp.split('|')[2].split('@')[1]+":"+smtp.split('|')[1]
            print(f"{Fore.YELLOW}[{Fore.CYAN}{current}{Fore.YELLOW}/{Fore.CYAN}{count}{Fore.YELLOW}] {Fore.YELLOW}{HOST} {Fore.RED}{file} {Fore.WHITE}{test} {color}{value}")
            if platform.system() == "Windows":
                try:
                    os.system(f"title Pending SMTP:[{count-current}]     Completed SMTP:[{current-error}]     Error SMTP:[{error}]")
                except:pass
                if type and value=="SMTP connect failed":quit()

def Tester():
  global count
  number=0
  file = scandir("file/Smtps")
  smtp = open(Exsist("file/Smtps/"+file),'r').read().split('\n')
  data = os.listdir("configuration")
  test = json.loads(open("Settings.json", "r").read())["Sender"]["test"]
  if not len(data):
      print(f"\n{Fore.RED}[x] {Fore.YELLOW}Files not found, you need to create a new configuration file")
      quit()
  print("")    
  for file in data:
      number+=1
      print(f"{Fore.CYAN} [{number}]: {Fore.MAGENTA}{file}")
  back = number+1 
  print(f"{Fore.CYAN} [{back}]: {Fore.YELLOW}All")     
  select = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
  if back == select:
     config = data
  else:            
     config = [data[select-1]]
  email = test.split(',')   
  count=len(smtp)
  short=len(email)
  print(f"\n{Fore.YELLOW}[Total Smtp]: {Fore.RED}{count}") 
  print(f"{Fore.YELLOW}[Total Email]: {Fore.RED}{short}") 
  thread = int(input(f"\n{Fore.YELLOW}[Thread]: {Fore.WHITE}")) 
  print("") 
  start= timer()  
  with ThreadPoolExecutor(thread) as pool:
     pool.map(Inbox,repeat(config),repeat(email), smtp) 
  print('\nTime: ',convert(timer()-start),"\n\n")      
 
def home():
  clear()
  banner()
  value,check = option()
  if platform.system() == "Windows":
      try:os.system(f"title {value}")
      except:pass
  if check == 1:
    return Create()
  elif check == 2:  
    return Editor("")
  elif check == 3:  
    return View()    
  elif check == 4:  
    return Remove()    
  elif check == 5:
    TryPHP()  
    return Validate()    
  elif check == 6:  
    TryPHP()
    return Sender()
  elif check == 7:  
    TryPHP()
    return Tester()
  elif check == 8:  
    return split_emails() 
  elif check == 9:  
    return duplicates()     
  elif check == 10:  
    if platform.system() == "Windows":os.system("Statistics.html")
  elif check == 11:  
    if platform.system() == "Windows":os.system("Random.html")
  elif check == 12:  
    if platform.system() == "Windows":os.system("start https://t.me/rotinabox")  
    else:print(f"\n{Fore.YELLOW}[Contact]: https://t.me/rotinabox") 
  elif check == 13:  
    quit() 
 
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def banner():
 print(f'''
{rotina}__  __      _       _ _                    ___  
{rotina}\ \/ /_ __ | | ___ (_) |_ ___ _ __ ___    / __\ __ _____      __
{rotina} \  /| '_ \| |/ _ \| | __/ _ \ '__/ __|  / / | '__/ _ \ \ /\ / /
{rotina} /  \| |_) | | (_) | | ||  __/ |  \__ \ / /__| | |  __/\ V  V /
{rotina}/_/\_\ .__/|_|\___/|_|\__\___|_|  |___/ \____/_|  \___| \_/\_/
{rotina}     | |
{rotina}     |_|
{rotina}
 ''')
 
def option():
 if platform.system() == "Windows":
     try:os.system(f"title SMTP Sender")
     except:pass
 text = ["Create A new configuration", "Edit configuration", "View configuration", "Remove configuration", "Validate SMTP", "Start Sender","Tester Inbox Sender",  "Split emails file", "Remove duplicates from list","Statics View", "Random View", "ABOUT TOOL", "Exit"]
 number=0
 for types in text:
   number+=1
   print(f"{Fore.CYAN}({number}) {Fore.LIGHTYELLOW_EX}{types}")
 zabi = int(input(f"\n{Fore.YELLOW}[Select]: {Fore.WHITE}"))
 return(text[zabi-1],zabi)
  
 
if __name__ == "__main__":
    init(autoreset=True)
    FORES = [Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]
    rotina = random.choice(FORES)
    key,current,event,success,error,bad,logs,currents = 0,0,0,0,0,0,0,1
    worker = True
    dragon = {}
    #azzouz = []
    pkg_install()
    home()
