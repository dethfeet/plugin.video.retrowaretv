import re, sys
import urllib, urllib2
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import showEpisode


#Retroware TV, XBMC add-on

#@author: Ricardo "Averre" Ocana Leal
#@version: 1.1.0

embedCats = ['retroactive-archive','retroactive-extras','retroactive-game-quickies','pat-the-nes-punk-archive']
unwanteds = ['podcast', 'retrobeat']

thisPlugin = int(sys.argv[1])
_regex_extractEpisode = re.compile("<li>.*?<div class=\"roknewspager-div\">(.*?)<a href=\"([^\"]*?)\" class=\"roknewspager-title\">(.*?)</a>.*?<div class=\"introtext\">(.*?)</div>.*?</li>",re.DOTALL)
_regex_extractEpisodeInfoImg = re.compile("<img src=\"(.*?)\" alt=\".*?\" />",re.DOTALL)

_regex_extractPageUrl = re.compile("'url': '(http://retrowaretv.com/wp-admin/admin-ajax.php\?action=roknewspager&id=widget-roknewspager-[0-9]*&offset=)_OFFSET_")
_regex_extractPageCount = re.compile("<li .*>([0-9]{1,3})</li>")

_regex_extractLatest = re.compile("<div id=\"featured\">(.*?)</div>[ \r\n]*</div>",re.DOTALL)
_regex_extractLatestEpisode = re.compile("<a href=\"([^\"]*?)\" title=\"([^\"]*?)\" target=\"_self\">[ \r\n]*<img [ \r\n]*src=\"([^\"]*?)\"[ \r\n]*alt=\"[^\"]*?\"[ \r\n]*/>[ \r\n]*</a>",re.DOTALL)

_regex_extractArchiveVideo = re.compile("<td><a title=\"([^\"]*?)\" href=\"([^\"]*?)\" ><img src=\"([^\"]*?)\" alt=\"\" width=\"150\" height=\"150\" /></a></td>")


def mainPage():
    addDirectoryItem('Latest Videos ',{'action':"listLatest","link":"http://retrowaretv.com/"})
    addDirectoryItem('Shows',{'action':"listShows"})
    addDirectoryItem('User Submissions',{'action':"listVideos",'link' : "http://retrowaretv.com/user-blogs/"})
    addDirectoryItem('Archive',{'action':"listArchive"})
        
def listShows():
    addDirectoryItem('16-Bit Gems',{'action':"listVideos",'link' : "http://retrowaretv.com/16-bit-gems/"},"http://retrowaretv.com/wp-content/uploads/2011/06/16bitsitebanner-300x84.png")
    addDirectoryItem('From Pixels To Plastic',{'action':"listVideos",'link' : "http://retrowaretv.com/pixels-to-plastic/"},"http://retrowaretv.com/wp-content/uploads/2011/06/P2P-Banner-300x128.gif")
    addDirectoryItem('The Game Chasers',{'action':"listVideos",'link' : "http://retrowaretv.com/the-game-chasers/"},"http://retrowaretv.com/wp-content/uploads/2011/07/gamechaserslogo.png")
    addDirectoryItem('Game Quickie',{'action':"listVideos",'link' : "http://retrowaretv.com/game-quickies/"},"http://retrowaretv.com/wp-content/uploads/2011/06/gquickie.png")
    addDirectoryItem('The Gaming Historian',{'action':"listVideos",'link' : "http://retrowaretv.com/the-gaming-historian/"},"http://retrowaretv.com/wp-content/uploads/2011/06/gaming-historian-banner1-300x76.gif")
    addDirectoryItem('Happy Video Game Nerd',{'action':"listVideos",'link' : "http://retrowaretv.com/happy-video-game-nerd/"},"http://retrowaretv.com/wp-content/uploads/2011/06/HVGN-2.0-sizeb1.png")
    addDirectoryItem('Let\'s Get!!',{'action':"listVideos",'link' : "http://retrowaretv.com/lets-get/"},"http://retrowaretv.com/wp-content/uploads/2011/06/letsgetbanner-300x189.png")
    addDirectoryItem('Pat The NES Punk',{'action':"listVideos",'link' : "http://retrowaretv.com/pat-the-nes-punk/"},"http://retrowaretv.com/wp-content/uploads/2011/06/PatNESLogo-300x196.jpg")
    addDirectoryItem('RetroActive',{'action':"listVideos",'link' : "http://retrowaretv.com/retroactive/"},"http://www.retrowaretv.com/wp-content/uploads/2011/06/retroactiverwtvbanner.png")
    addDirectoryItem('RetrowareTV The Show',{'action':"listVideos",'link' : "http://retrowaretv.com/retrowaretv-the-show/"},"http://retrowaretv.com/wp-content/uploads/2011/06/rwtvthe-show-logo.png")
    addDirectoryItem('Sold Separately',{'action':"listVideos",'link' : "http://retrowaretv.com/sold-separately/"},"http://retrowaretv.com/wp-content/uploads/2011/06/sold-separately-banner.gif")
    addDirectoryItem('Videogame Knowledge',{'action':"listVideos",'link' : "http://retrowaretv.com/video-game-knowledge/"},"http://retrowaretv.com/wp-content/uploads/2011/06/videogame-knowledge-banner.gif")

def ListArchive():    
    addDirectoryItem('Jam Enslaver',{'action':"listArchiveVideos",'link' : "http://retrowaretv.com/jam-enslaver-2/"},"http://theitochannel.com/wp-content/uploads/2011/06/jamenslaver1.png")

def ListLatest(url):
    link = LoadPage(url)
    latestDiv = _regex_extractLatest.search(link)
    if latestDiv is not None:
        for latestItem in _regex_extractLatestEpisode.finditer(latestDiv.group(1)):
            url = latestItem.group(1).strip()
            name = latestItem.group(2).strip()
            thumbnail = latestItem.group(3).strip()
            embed = True
            for unwanted in unwanteds:
                if url.find(unwanted) is not -1:
                    embed = False
                    
            if embed:
                name = remove_html_special_chars(name)
                url = url.replace("../","http://retrowaretv.com/")
                thumbnail = thumbnail.replace("../","http://retrowaretv.com/")
                addDirectoryItem(name,{'action':"playEpisode",'link':url},thumbnail,False)
            
def listVideos(url):
    link = LoadPage(url)
    
    ajax_url = _regex_extractPageUrl.search(link).group(1)
    ajax_pages = _regex_extractPageCount.findall(link)
    
    for i in ajax_pages:
        url = ajax_url+str((int(i)-1)*5)
        link = LoadPage(url)
        
        for videoItem in _regex_extractEpisode.finditer(link):
            videoItemImgItem = _regex_extractEpisodeInfoImg.search(videoItem.group(1))
            name = videoItem.group(3)
            url = videoItem.group(2)
            description = videoItem.group(4)
            thumbnail = ''
            if videoItemImgItem is not None:
                thumbnail = videoItemImgItem.group(1)
            name = remove_html_special_chars(name)
            url = url.replace("../","http://retrowaretv.com/")
            thumbnail = thumbnail.replace("../","http://retrowaretv.com/")
            addDirectoryItem(name,{'action':"playEpisode",'link':url},thumbnail,False)

def listArchiveVideos(url):
    link = LoadPage(url)
    
    for videoItem in _regex_extractArchiveVideo.finditer(link):
        name = videoItem.group(1)
        url = videoItem.group(2)
        thumbnail = videoItem.group(3)
        name = remove_html_special_chars(name)
        url = url.replace("../","http://retrowaretv.com/")
        thumbnail = thumbnail.replace("../","http://retrowaretv.com/")
        addDirectoryItem(name,{'action':"playEpisode",'link':url},thumbnail,False)

def playEpisode(url):
    episode_page = LoadPage(url)
    showEpisode.showEpisode(episode_page)

def showEpisodeBip(url):    
    #GET the 301 redirect URL
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    fullURL = response.geturl()
    
    feedURL = _regex_extractVideoFeedURL.search(fullURL)
    if feedURL is None:
        feedURL = _regex_extractVideoFeedURL2.search(fullURL)
    feedURL = urllib.unquote(feedURL.group(1))
    
    blipId = feedURL[feedURL.rfind("/")+1:]
    
    stream_url = "plugin://plugin.video.bliptv/?action=play_video&videoid=" + blipId
    item = xbmcgui.ListItem(path=stream_url)
    return xbmcplugin.setResolvedUrl(thisPlugin, True, item)

def showEpisodeYoutube(youtubeID):
    stream_url = "plugin://plugin.video.youtube/?action=play_video&videoid=" + youtubeID
    print stream_url;
    item = xbmcgui.ListItem(path=stream_url)
    xbmcplugin.setResolvedUrl(thisPlugin, True, item)
    return False

def LoadPage(url):
    print url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    return link

def remove_html_special_chars(input):
    input = input.replace("&#8211;","-")
    input = input.replace("&#8217;","'")#\x92
    input = input.replace("&#039;",chr(39))# '
    input = input.replace("&#038;",chr(38))# &
    input = input.replace("&amp;",chr(38))# &
    input = input.replace(r"&quot;", "\"")
    input = input.replace(r"&apos;", "\'")
    input = input.replace(r"&#8217;", "\'")
    input = input.replace(r"&#8230;", "...")
    
    return input

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addDirectoryItem(name, parameters={}, pic="", folder=True):
    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=pic)
    if not folder:
        li.setProperty('IsPlayable', 'true')
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=folder)
              

if not sys.argv[2]:
    mainPage()
else:
    params=get_params()
    if params['action'] == "listShows":
        listShows()
    elif params['action'] == "listArchive":
        ListArchive()
    elif params['action'] == "listLatest":
        ListLatest(urllib.unquote(params['link']))
    elif params['action'] == "listVideos":
        listVideos(urllib.unquote(params['link']))
    elif params['action'] == "listArchiveVideos":
        listArchiveVideos(urllib.unquote(params['link']))
    elif params['action'] == "playEpisode":
        playEpisode(urllib.unquote(params['link']))
    else:
        mainPage()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
