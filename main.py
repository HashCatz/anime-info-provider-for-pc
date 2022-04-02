import requests
import os
import queries

#https://www.youtube.com/results?search_query=naruto
def shorten(description, info='anilist.co'):
    msg = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        msg += f'<br> _{description}_<a href="{info}">Read More</a>'
    else:
        msg += f"<br>_{description}_"
    return msg

def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]

url = 'https://graphql.anilist.co'
while True:
    print("""
░█████╗░███╗░░██╗██╗███╗░░░███╗███████╗  ██╗███╗░░██╗███████╗░█████╗░
██╔══██╗████╗░██║██║████╗░████║██╔════╝  ██║████╗░██║██╔════╝██╔══██╗
███████║██╔██╗██║██║██╔████╔██║█████╗░░  ██║██╔██╗██║█████╗░░██║░░██║
██╔══██║██║╚████║██║██║╚██╔╝██║██╔══╝░░  ██║██║╚████║██╔══╝░░██║░░██║
██║░░██║██║░╚███║██║██║░╚═╝░██║███████╗  ██║██║░╚███║██║░░░░░╚█████╔╝
╚═╝░░╚═╝╚═╝░░╚══╝╚═╝╚═╝░░░░░╚═╝╚══════╝  ╚═╝╚═╝░░╚══╝╚═╝░░░░░░╚════╝░

██████╗░██████╗░░█████╗░██╗░░░██╗██╗██████╗░███████╗██████╗░
██╔══██╗██╔══██╗██╔══██╗██║░░░██║██║██╔══██╗██╔════╝██╔══██╗
██████╔╝██████╔╝██║░░██║╚██╗░██╔╝██║██║░░██║█████╗░░██████╔╝
██╔═══╝░██╔══██╗██║░░██║░╚████╔╝░██║██║░░██║██╔══╝░░██╔══██╗
██║░░░░░██║░░██║╚█████╔╝░░╚██╔╝░░██║██████╔╝███████╗██║░░██║
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝
Version: 0.2                                       By HashCatz
"""+"\n\nWhat Do You Want To Search?\n\n1 = Anime Info\n2 = Manga Info\n3 = Airing Dates\n4 = Character Info\n5 = About Us\n\nIf You want to Leave Type 'Stop'")
    try:
        getting_id=int(input("\nEnter The Number :"))
    except:
        print("\nEnter  A Number")
        continue
    if getting_id==1:
        while True:
            search = str(input("\nEnter The Name Of The Anime: "))
            search=search.lower()
            if search =="stop":
                break    
            if len(search) == 0:
                print("\nEnter The Name Baaaka!")
                continue
            else:
                try:
                        variables = {'search': search}
                        json = requests.post(
                                url, json={
                                    'query': queries.anime_query,
                                    'variables': variables
                                }).json()
                        if 'errors' in json.keys():
                            print('\nAnime not found Check The Spellings Or Search Using The Japanese name')
                        if json:
                                json = json['data']['Media']
                                msg = f"\n{json['title']['romaji']}({json['title']['native']})\n\n-> Country Of Origin: {json['countryOfOrigin']}\n\n-> Type: {json['format']}\n\n-> Status: {json['status']}\n\n-> Episodes: {json.get('episodes', 'N/A')}\n\n-> Duration: {json.get('duration', 'N/A')} Per Ep.\n\n-> Score: {json['averageScore']}\n\n-> Genres: `"
                                for x in json['genres']:
                                    msg += f"{x}, "
                                msg = msg[:-2] + '`\n'
                                msg += "\n-> Studios: "
                                for x in json['studios']['nodes']:
                                    msg += f"{x['name']}, "
                                msg = msg[:-2] + '\n'
                                msg += "\n-> Next Episode: "
                                if json['nextAiringEpisode']:
                                    time = json['nextAiringEpisode']['timeUntilAiring'] * 1000
                                    time = t(time)
                                    msg += f"\n\n-> Airing Episode: {json['nextAiringEpisode']['episode']}\n\n-> Airing In: {time}"
                                else:
                                    msg += f"Finished"
                                msg = msg[:-2] + '\n'
                                info = json.get('siteUrl')
                                trailer = json.get('trailer', None)
                                anime_id = json['id']
                                if trailer:
                                    trailer_id = trailer.get('id', None)
                                    site = trailer.get('site', None)
                                    if site == "youtube":
                                        trailer = 'https://youtu.be/' + trailer_id
                                description = json.get('description', 'N/A').replace('<i>', '').replace(
                                    '</i>', '').replace('<br>', '')
                                msg += shorten("\n\nDescription:\n\n"+description, info)
                                image = json.get('bannerImage', None)
                                #if trailer:
                                    #print(info)
                                    #print(trailer)
                                #else:
                                    #print(info)
###################################                               ###################3###################################################################3     
                                htm = f"""
<!DOCTYPE html>
<html>
<head>
<title>{json['title']['romaji']}({json['title']['native']})</title>
<link rel="shortcut icon" type="image/x-icon" href="./css/logo.png" />
<link rel="stylesheet" href="./css/Style.css">
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="./css/all.css">


    <!-- Custom Style   -->
    <link rel="stylesheet" href="./css/Style.css">
</head>
<body>
    <nav class="nav">
        <div class="nav-menu flex-row">
            <div class="nav-brand">
                <a href="https://github.com/HashCatz" class="text-gray">HasH Catz</a>
            </div>
            <div class="toggle-collapse">
                <div class="toggle-icons">
                    <i class="fas fa-bars"></i>
                </div>
            </div>
            <div>
                <ul class="nav-items">
                    <li class="nav-link">
                        <a href="#">Home</a>
                    </li>
                </ul>
            </div>
            <div class="social text-gray">
                <a href="https://t.me/troj3n"><i class="fab fa-telegram"></i></a>
                <a href="https://github.com/TR0J3N"><i class="fab fa-github"></i></a>
                <a href="https://www.instagram.com/t_r_o_j_3_n"><i class="fab fa-instagram"></i></a>
            </div>
        </div>
    </nav>
<main>

<h1><center>{json['title']['romaji']}({json['title']['native']})</center></h1>
<img src="{image}" alt="{image}"></img>
<section class="info">  
<div class="tit"><center>𝚃𝚢𝚙𝚎: {json['format']}<br></center></div>
<div class="tit"><center>𝙲𝚘𝚞𝚗𝚝𝚛𝚢 𝙾𝚏 𝙾𝚛𝚒𝚐𝚒𝚗: {json['countryOfOrigin']}<br></center></div>
<div class="tit"><center>𝚂𝚝𝚊𝚝𝚞𝚜: {json['status']}<br></center></div>
<div class="tit"><center>𝙴𝚙𝚒𝚜𝚘𝚍𝚎𝚜: {json.get('episodes', 'N/A')}<br></center></div>
<div class="tit"><center>𝙳𝚞𝚛𝚊𝚝𝚒𝚘𝚗: {json.get('duration', 'N/A')} Per Ep.<br></center></div>
<div class="tit"><center>𝚂𝚌𝚘𝚛𝚎: {json['averageScore']}<br></center></div>
<div class="tit"><center>𝙶𝚎𝚗𝚛𝚎𝚜:

    <!-- Jquery Library file -->
    <script src="./js/Jquery3.4.1.min.js"></script>

    <!-- --------- Owl-Carousel js ------------------->
    <script src="./js/owl.carousel.min.js"></script>

    <!-- ------------ AOS js Library  ------------------------- -->
    <script src="./js/aos.js"></script>

    <!-- Custom Javascript file -->
    <script src="./js/main.js"></script>
	
"""
                                for x in json['genres']:
                                    htm += f"{x}, "
                                htm = htm[:-2] + '\n'
                                htm += "<div class='tit'><center>𝚂𝚝𝚞𝚍𝚒𝚘𝚜: "
                                for x in json['studios']['nodes']:
                                    htm += f"{x['name']}, "
                                htm = htm[:-2] + '<br>'
                                htm += "<br>𝙽𝚎𝚡𝚝 𝙴𝚙𝚒𝚜𝚘𝚍𝚎: "
                                if json['nextAiringEpisode']:
                                    time = json['nextAiringEpisode']['timeUntilAiring'] * 1000
                                    time = t(time)
                                    htm += f"""<br>&nbsp-->𝙴𝚙𝚒𝚜𝚘𝚍𝚎: {json['nextAiringEpisode']['episode']}<br>&nbsp-->𝙰𝚒𝚛𝚒𝚗𝚐 𝙸𝚗: {time}"""
                                else:
                                    htm += f"Finished"
                                htm = htm[:-2] + '\n'                                
                                inf = json.get('siteUrl')
                                traile = json.get('trailer', None)
                                anime_id = json['id']
                                if traile:
                                    traile_id = traile.get('id', None)
                                    site = traile.get('site', None)
                                    if site == "youtube":
                                        traile = 'https://youtu.be/' + traile_id
                                description = json.get('description', 'N/A').replace('<br>', '').replace(
                                    '<br>', '').replace('<br>', '')
                                #if trailer:
                                   # print(info)
                                    #print(trailer)
                                #else:
                                    #print(info)
                                htm += shorten("<h2>𝘿𝙚𝙨𝙘𝙧𝙞𝙥𝙩𝙞𝙤𝙣;</h2><br><p align='center'>"+description+"</p>", inf)
######################################################################################################
                        text = open(search+'.html','w',encoding="utf-8")
                        text.write(htm+"<br>"+"<section class='buttn'><center><button class='btn'><a href='"+info+"'><div class='textx'>More Info</div></a></button></center><div class='downl'>Download Links</div><button class='btn'><a href='https://www.wcostream.com/search/"+search+"'>Wco Stream</a></button><button class='btn'><a href='https://kissanimes.pro/search/"+search+"/'><center>Kiss Anime</center></a></button><div class='downl'>Additional</div><button class='btn'><a href='https://www.youtube.com/results?search_query="+search+" trailer'><center>Trailer</center></a></button><button class='btn'><a href='https://www.youtube.com/results?search_query="+search+" op'><center>Opening</center></a></button><button class='btn'><a href='https://www.youtube.com/results?search_query="+search+" ED'><center>Ending</center></a></button></section></main>"+"""
 <footer class="footer">
        <div class="container">
            <div class="about-us" data-aos="fade-right" data-aos-delay="200">
                <h2>About us</h2>
                <p>We Are Two Lonely Catz Who Build Programs..<br>
                    Devs:<br>
                          <i>--> TROJ3N<br></i>
                          <i>--> Dulnith_Liyanage<br></i>
                </p>
            </div>
            <div class="newsletter" data-aos="fade-right" data-aos-delay="200">
                <h2>Updates</h2>
                <p>Stay updated with our latest</p>
                <div class="form-element">
                    <p>Our Community</p></span>
                    <button class="btn footer-btn"><a href="https://github.com/HashCatz">Here!</a></button>
                </div>
            </div>
            <div class="instagram" data-aos="fade-left" data-aos-delay="200">
                <div class="logo">
                    <img src="./css/logo.png">
                </div>
            </div>
            <div class="follow" data-aos="fade-left" data-aos-delay="200">
                <h2>Follow us</h2>
                <p>Let us be Social</p>
                <div>
                    <a href="https://github.com/TR0J3N"><i class="fab fa-github"></i></a>
                    <a href="https://t.me/troj3n"><i class="fab fa-telegram"></i></a>
                    <a href="https://www.instagram.com/t_r_o_j_3_n"><i class="fab fa-instagram"></i></a>
                </div>
            </div>
        </div>
        <div class="rights flex-row">
            <h4 class="text-gray">
                Copyright ©2022 All rights reserved | made by
                <a href="https://t.me/troj3n" target="_black">TR0J3N</a>
            </h4>
        </div>
    </footer>

</html></body>""")
                        text.close()
                        print("\n"+msg+"\n\n"+"More info Here: "+info+"\nIf There is an Image It will download"+"""\n\n
___________________________________________________
|                                                 |
| Check The HTML file That Saved in the Directory | 
|                                                 |
---------------------------------------------------

Anime Info Collected By HasHCatz
--> https://github.com/HashCatz <--
""")
                        
                        if image:
                                try:
                                    response = requests.get(f"{image}")
                                    file = open(search+".jpg", "wb")
                                    file.write(response.content)
                                    print("\n\nThere is A picture in the directory check it too..")
                                except:
                                    print("There Aint Any Images!")
                        else:
                            print("There Aint Any Images!")
                        os.system(search+".html")
                        leave=input("\n\nWanna Continue? Y/N : ")
                        leave=leave.lower()
                        if len(leave) == 0:
                            print("Closing The Terminal...")
                            break
                        elif leave=="y":
                            continue
                        elif leave=="n":
                            break
                        else:
                            print("Closing The Terminal...")
                            break
                except:
                    print("Check Your Network Connection!")
                    ############################3------------------airing-----------------#####################333333
    elif getting_id==3:                
        while True:
            try:
                airing=input("Enter A name of an anime: ")
                airing = airing.lower()
                if airing =="stop":
                    break
                if len(airing) == 0:
                    print("\nEnter The Name Baaaka!")
                    continue
                else:
                    variables = {'search': airing}
                    response = requests.post(
                        url, json={
                            'query': queries.airing_query,
                            'variables': variables
                        }).json()['data']['Media']
                    msg = f"\n\nName: {response['title']['romaji']}({response['title']['native']})\n\n-> ID: {response['id']}"
                    if response['nextAiringEpisode']:
                        time = response['nextAiringEpisode']['timeUntilAiring'] * 1000
                        time = t(time)
                        msg += f"\n\n-> Episode: {response['nextAiringEpisode']['episode']}\n\n-> Airing In: {time}"
                    else:
                        msg += f"\n\n-> Episode: {response['episodes']}\n\n-> Status: N/A"
                    print(msg+"\n\nAiring Dates Collected By HashCatz\n--> https://github.com/HashCatz<--")
                    leave=input("\n\nWanna Continue? Y/N : ")
                    leave=leave.lower()
                    if len(leave) == 0:
                        print("====>> Closing The Terminal! <<====")
                        break
                    elif leave=="y":
                        continue
                    elif leave=="n":
                        break
                    else:
                        print("====>> Closing The Terminal! <<====")
                        break
            except:
                    print("Check your Network connection and try again!")
                    continue
                ###########################------------------------manga--------------------#####################################33
    elif getting_id==2:
        while True:
            try:
                manga=input("Enter A name of an manga: ")
                manga = manga.lower()
                if manga =="stop":
                    break
                if len(manga) == 0:
                    print("\nEnter The Name Baaaka!")
                else:
                    variables = {'search': manga}
                    json = requests.post(
                        url, json={
                            'query': queries.manga_query,
                            'variables': variables
                        }).json()
                    msg = ''
                    if 'errors' in json.keys():
                        print('Manga not found')
                    if json:
                        json = json['data']['Media']
                        title, title_native = json['title'].get('romaji',
                                                                False), json['title'].get(
                                                                    'native', False)
                        start_date, status, score, country ,chaps ,vols, fomat, adult= json['startDate'].get(
                            'year', False), json.get('status',
                                                     False), json.get('averageScore', False), json.get('countryOfOrigin', False), json.get('chapters', False), json.get('volumes',False), json.get('format',False), json.get('isAdult', False)
                        if title:
                            msg += f"\n-------------------------------------------------\n{title}"
                            if title_native:
                                msg += f"(`{title_native}`)"
                        if country:
                            msg += f"\n\n-> Country Of Origin - {country}"
                        if start_date:
                            msg += f"\n\n-> Start Date - {start_date}"
                        if status:
                            msg += f"\n\n-> Status - {status}`"
                        if score:
                            msg += f"\n\n-> Score - {score}"
                        if chaps:
                            msg  += f"\n\n-> Chapters - {chaps}"
                        if vols:
                            msg +=f"\n\n-> Volumes - {vols}"
                        if fomat:
                            msg+=f"\n\n-> Format - {fomat}"
                        if adult:
                             msg+=f"\n\n-> Adult Rated - {adult}"
                        msg += '\n\n-> Genres - '
                        for x in json.get('genres', []):
                            msg += f"{x}, "
                        msg = msg[:-2]
                        info = json['siteUrl']
                        if info:
                            msg+=f"\n\n-> More Info - "+info
                        image = json.get("bannerImage", None)
                        msg += f"\n\nDescription:\n\n{json.get('description', None)}_"
                        print(msg+"""

___________________________________________________
|                                                 |
| Check The TXT file That Saved in the Directory  | 
|                                                 |
---------------------------------------------------

Manga Info Collected By HasHCatz
--> https://github.com/HashCatz <--
""")
                        text = open(manga+' manga.txt','w',encoding="utf-8")
                        text.write(msg)
                        text.close()
                        leave=input("\n\nWanna Continue? Y/N : ")
                        leave=leave.lower()
                        if len(leave) == 0:
                            print("====>> Closing The Terminal! <<====")
                            break
                        elif leave=="y":
                            continue
                        elif leave=="n":
                            break
                        else:
                            print("====>> Closing The Terminal! <<====")
                            break
                        
            except:
                print("Check Your Network Connection and try again")
                
    elif getting_id==5:
        print("""
About Us...
Devs:
    -> TR0J3N Kaizenix
    -> dulnithLiyanage
    
Description:
We Are Two Sri Lankan Programmers Who Build Programs.You Can Get Our Repos From : https://github.com/HashCatz

Languages and Scripts Used:
    => Python
    => HTML
    => CSS

Python Libs That Used:
    --> Requests
    --> OS

API That Used:
    ~> https://anilist.co

Websites Which Used:
    >> https://www.wcostream.com
    >> https://kissanimes.pro
    >> https://www.youtube.com

*Note*
There Will be Some New Updates So Stay Tuned..

""")
        continue
    elif getting_id==4:
        while True:
            try:
                search=input("Enter The Name Of The Character: ")
                search = search.lower()
                if search =="stop":
                    break
                if len(search) == 0:
                    print("\nEnter The Name Baaaka!")
                else: 
                    variables = {'query': search}
                    json = requests.post(
                        url, json={
                            'query': queries.character_query,
                            'variables': variables
                        }).json()
                    if 'errors' in json.keys():
                        print('Character not found')
                        continue
                    if json:
                        json = json['data']['Character']
                        msg = f"\n\n{json.get('name').get('full')}({json.get('name').get('native')})\n\n"
                        description = f"Description:\n\n{json['description']}"
                        site_url = json.get('siteUrl')
                        msg += shorten(description, site_url)
                        image = json.get('image', None)
                    print(msg)
                    if image:
                            try:
                                response = requests.get(f"{image}")
                                file = open(search+".jpg", "wb")
                                file.write(response.content)
                                print("\n\nThere is A picture in the directory check it too..")
                            except:
                                print("There Aint Any Images!")
                    leave=input("\n\nWanna Continue? Y/N : ")
                    leave=leave.lower()
                    if len(leave) == 0:
                        print("====>> Closing The Terminal! <<====")
                        break
                    elif leave=="y":
                        continue
                    elif leave=="n":
                        break
                    else:
                        print("====>> Closing The Terminal! <<====")
                        break                    
            except:
                print("Check Your Network Connection and try again")
                
                
    else:
        print("\n\nEnter A Valid Number!!")
    left=input('If you want to close the terminal Type Y else Press Enter\n>>>')
    left=left.lower()
    if left=="y":
        print("====>> Closing The Terminal! <<====")
        break
    elif not left=="y":
        print("\n------> Continuing <------")
        continue
    else:
        continue

