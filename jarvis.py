import pyttsx3
import speech_recognition as sr
import random
import datetime
import wikipedia
import webbrowser
from bs4 import BeautifulSoup    #for search query
import requests
import os
import smtplib

#set proporties of speak engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice',voices[0].id)

class person:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms,query):
    for term in terms:
        if term in query:
            return True

#For Google Search
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 17:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    greetings = ["hey! I am Jarvis, how can I help you" + person_obj.name, "hey! I am Jarvis, what's up?" + person_obj.name, "I'm listening" + person_obj.name, "how can I help you?" + person_obj.name, "hello I am Jarvis" + person_obj.name]
    greet = greetings[random.randint(0,len(greetings)-1)]
    speak(greet)
    

def takeCmd():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        #print(e)
        print("Say That again please...")
        return "NONE"
    
    return query


#Search Result from google
def googleSearch(query):
    query = query.replace(" ","+")
    try:
        url = f'https://www.google.com/search?q={query}&oq={query}&aqs=chrome..69i57j46j69i59j35i39j0j46j0l2.4948j0j7&sourceid=chrome&ie=UTF-8'
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
    except:
        print("Make sure you have a internet connection")
        speak("Make sure you have a internet connection")
    try:
        try:
            ans = soup.select('.RqBzHd')[0].getText().strip()
        
        except:
            try:
                title=soup.select('.AZCkJd')[0].getText().strip()
                try:
                    ans=soup.select('.e24Kjd')[0].getText().strip()
                except:
                    ans=""
                ans=f'{title}\n{ans}'
                
            except:
                try:
                    ans=soup.select('.hgKElc')[0].getText().strip()
                except:
                    ans=soup.select('.kno-rdesc span')[0].getText().strip()
    
    except:
        ans = "Sorry! can't find on google"
    return ans


def sendEmail(to,content):
    #using SMTP lib module we can send mail using gmail
    #to use this we need to enable our less secure apps
    server = smtplib.SMTP('smpt.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('yourmail@gmail.com','my-password')
    server.sendmail('yourmail@gmail.com',to,content)
    server.close()

if __name__ == "__main__":
    person_obj = person()
    #1.greetings
    wishMe()
                
    try:
        while True:
            query = takeCmd().lower()

            #2.Name
            if there_exists(["what is your name","what's your name","tell me your name"],query):
                speak("My name is Jarvis . what's your name?")

            if there_exists(["my name is"],query):
                person_name = query.split("is")[-1].strip()
                speak("okay, i will remember that " + person_name)
                person_obj.setName(person_name)

            if there_exists(["how are you","how are you doing"],query):
                speak("I'm very well, thanks for asking " + person_obj.name)

            #3.Search Wikipedia
            if 'wikipedia' in query:
                speak('Searching Wikipedia... Please Wait!')
                query = query.replace("wikipedia","")
                results = wikipedia.summary(query,sentences=3)
                speak("According to Wikipedia...")
                #print(results)
                speak(results)
            
            #4.Search Google 
            if there_exists(["search for"],query) and 'youtube' not in query:
                search_term = query.split("for")[-1]
                url = "https://google.com/search?q=" + search_term
                webbrowser.get().open(url)
                speak("Here is what I found for" + search_term + "on google")

            # 5: search youtube
            if there_exists(["youtube"],query):
                search_term = query.split("for")[-1]
                url = "https://www.youtube.com/results?search_query=" + search_term
                webbrowser.get().open(url)
                speak("Here is what I found for " + search_term + "on youtube")

            #6.Find defination
            if 'defination of' in query:
                query = query.replace("search","")
                result = googleSearch(query)
                print(result)
                speak(result)

            #7.search for amazon.com
            if 'open amazon' in query:
                search_term = query.split("for")[-1]
                url="https://www.amazon.in"+search_term
                webbrowser.get().open(url)
                speak("here is what i found for amazon.com")

            #8.make a note
            if 'make a note' in query:
                search_term=query.split("for")[-1]
                url="https://keep.google.com/#home"
                webbrowser.get().open(url)
                speak("Here you can make notes")

            #9 weather
            if 'weather report' in query:
                search_term = query.split("for")[-1]
                url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
                webbrowser.get().open(url)
                speak("Here is what I found for wheather on google")

            #10.Open other Browsers
            if 'open youtube' in query:
                webbrowser.open("youtube.com")
                speak("here is what i found for youtube")
            if 'open google' in query:
                webbrowser.open("google.com")
                speak("here is what i found for google")
            if 'open stackoverflow' in query:
                webbrowser.open("stackoverflow.com")
                speak("here is what i found for stack over flow")
            if 'open twitter' in query:
                webbrowser.open("twitter.com")
                speak("here is what i found for twitter")
            if 'open instagram' in query:
                webbrowser.open("instagram.com")
                speak("here is what i found for instagram")
            if 'open whatsapp' in query:
                webbrowser.open("whatsapp.com")
                speak("here is what i found for whatsapp")
            if 'open gmail' in query:
                webbrowser.open("gmail.com")
                speak("here is what i found for gmail")
            if 'open linkedin' in query:
                webbrowser.open("linkedin.com")
                speak("here is what i found for linkedin")
            if 'open github' in query:
                webbrowser.open("github.com")
                speak("here is what i found for github")
            if 'open hackerrank' in query:
                webbrowser.open("hackerrank.com")
                speak("here is what i found for hackerrank")
            if 'open news' in query:
                webbrowser.open("news.com")
                speak("here is what i found for news.com")
            if 'open map' in query:
                webbrowser.open("map.com")
                speak("here is what i found for Google map")
            if 'open google drive' in query:
                webbrowser.open("drive.com")
                speak("here is what i found for google drive")

            #11.Play Music
            if 'play song' in query:
                music_dir = 'D:\\Music\\new music'
                songs = os.listdir(music_dir)
                total_song = len(songs)
                print(songs)
                for i in range(total_song):
                    os.startfile(os.path.join(music_dir,songs[i]))

            #12.To get time
            if 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H: %M: %S")
                speak(f"Sir, The time is {strTime}")

            #13.To open Applications from PC
            if 'open code' in query:
                code_path = "C:\\Users\\OCAC\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(code_path)
                speak("opening visual studio code")

            if 'open proteus' in query:
                code_path = "C:\\Program Files (x86)\\Labcenter Electronics\\Proteus 8 Professional\\BIN\\PDS.EXE"
                os.startfile(code_path)
                speak("opening proteus")

            if 'open zoom' in query:
                code_path = "C:\\Users\\OCAC\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"
                os.startfile(code_path)
                speak("opening zoom app")

            if 'open git' in query:
                code_path = "C:\\Users\\OCAC\\AppData\\Local\\GitHubDesktop\\GitHubDesktop.exe"
                os.startfile(code_path)
                speak("opening github desktop application")

            if 'open power point' in query:
                code_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
                os.startfile(code_path)
                speak("opening micro soft power point")

            if 'open MS word' in query:
                code_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE"
                os.startfile(code_path)
                speak("opening micro soft word")

            if 'open excell' in query:
                code_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
                os.startfile(code_path)
                speak("opening microsoft excell")

            if 'open photos' in query:
                code_path = "C:\\Users\\OCAC\\Pictures"
                os.startfile(code_path)
                speak("opening galary")

            #14.send email
            if 'email to someone' in query:
                try:
                    speak("what should i say...")
                    content = takeCmd()
                    to = "micky1987@gmail.com"
                    sendEmail(to,content)
                    speak("Hay! Your Email has been set...")
                except Exception as e:
                    print(e)
                    speak("Sorry Sir, I am not able to send the mail due to some issue")

            #15.stone paper scisorrs
            if 'stone game' in query:
                print("choose among rock paper or scissor")
                query = takeCmd()

                moves=["rock", "paper", "scissor"]
    
                cmove=random.choice(moves)
                pmove= query
        

                speak("The computer chose " + cmove)
                speak("You chose " + pmove)
                #engine_speak("hi")
                if pmove==cmove:
                    speak("the match is draw")
                elif pmove== "rock" and cmove== "scissor":
                    speak("Player wins")
                elif pmove== "rock" and cmove== "paper":
                    speak("Computer wins")
                elif pmove== "paper" and cmove== "rock":
                    speak("Player wins")
                elif pmove== "paper" and cmove== "scissor":
                    speak("Computer wins")
                elif pmove== "scissor" and cmove== "paper":
                    speak("Player wins")
                elif pmove== "scissor" and cmove== "rock":
                    speak("Computer wins")

            #16.toss a coin
            if 'toss coin game' in query:
                moves=["head", "tails"]   
                cmove=random.choice(moves)
                speak("The computer chose " + cmove)

            #17.calculation
            if there_exists(["plus","minus","multiply","divide","power","+","-","*","/"],query):
                opr = query.split()[1]

                if opr == '+':
                    speak(int(query.split()[0]) + int(query.split()[2]))
                elif opr == '-':
                    speak(int(query.split()[0]) - int(query.split()[2]))
                elif opr == 'multiply':
                    speak(int(query.split()[0]) * int(query.split()[2]))
                elif opr == 'divide':
                    speak(int(query.split()[0]) / int(query.split()[2]))
                elif opr == 'power':
                    speak(int(query.split()[0]) ** int(query.split()[2]))
                else:
                    speak("Wrong Operator")
        
            #18.Exit
            if there_exists(["exit", "quit", "goodbye"],query):
                speak("we could continue more, but as your wish sir! byee")
                exit()


    except KeyboardInterrupt:
        print("press ctrl+c to terminate")                

        



