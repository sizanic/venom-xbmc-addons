#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog

import urllib, json

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'ZT1_org'
SITE_NAME = 'Zone-telechargement-1'
SITE_DESC = 'Films Séries Animés'
URL_MAIN = 'https://zone-telechargement-1.org/'


# MOVIE_NEWS = (URL_MAIN + 'nouveaute/', 'showMovies') # films (derniers ajouts)
# MOVIE_EXCLUS = (URL_MAIN + 'exclus/', 'showMovies') # exclus (films populaires)
# MOVIE_3D = (URL_MAIN + 'films-bluray-3d/', 'showMovies') # films en 3D
# MOVIE_HD = (URL_MAIN + 'films-bluray-hd/', 'showMovies') # films en HD
# MOVIE_HDLIGHT = (URL_MAIN + 'x265-x264-hdlight/', 'showMovies') # films en x265 et x264
# MOVIE_VOSTFR = (URL_MAIN + 'filmsenvostfr/', 'showMovies') # films VOSTFR
# MOVIE_4K = (URL_MAIN + 'film-ultra-hd-4k/', 'showMovies') # films "4k"
# MOVIE_GENRES = (URL_MAIN , 'showGenre')
# MOVIE_ANIME = (URL_MAIN + 'dessins-animes/', 'showMovies') # dessins animes
# MOVIE_BDRIP = (URL_MAIN + 'films-dvdrip-bdrip/', 'showMovies')
# MOVIE_TS_CAM = (URL_MAIN + 'scrr5tscam-films-2017/', 'showMovies')
# MOVIE_VFSTFR = (URL_MAIN + 'films-vfstfr/', 'showMovies')
# MOVIE_MKV = (URL_MAIN + 'films-mkv/', 'showMovies')
# MOVIE_VO = (URL_MAIN + 'films-vo/','showMovies')
# MOVIE_INTEGRAL = (URL_MAIN + 'collection-films-integrale/','showMovies')

MOVIES_PER_PAGE = 25

MOVIE_GENRES = (URL_MAIN + 'wp-json/wp/v2/categories?per_page=100', 'showGenre')
MOVIE_URL = (URL_MAIN + 'wp-json/wp/v2/posts?per_page='+str(MOVIES_PER_PAGE)+'&categories=')
TAGS_URL = (URL_MAIN + 'wp-json/wp/v2/tags/')
POST_URL = (URL_MAIN + 'wp-json/wp/v2/posts/')
QUALITE_URL = (URL_MAIN + 'wp-json/wp/v2/posts?tags=')



def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText + '&search_start=1'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


# Récupération dynamique des catégories
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()
     
    contents = json.loads(sHtmlContent)
 
    if contents:
        progress_ = progress().VScreate(SITE_NAME)
        total = len(contents)
        for content in contents:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = content['name'].encode('utf-8')
            sUrl2 = MOVIE_URL + str(content['id'])
     
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
             
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        progress_.VSclose(progress_)
 
    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    numPage = oInputParameterHandler.getValue('numPage')
    if not numPage:
        numPage = 1

    oRequestHandler = cRequestHandler(sUrl+'&page='+ str(numPage))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()
    
    contents = json.loads(sHtmlContent)

    tags = set()

    if contents:
        
        # Chaque titre de film correspond à un tag
        # filtrer par tag unique (ne pas tenir compte de la qualité
        for content in contents:
            idTag = content['tags']
            tags.add(idTag[0])

        progress_ = progress().VScreate(SITE_NAME)
        total = len(tags)
        for tag in tags:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            oRequestHandler = cRequestHandler(TAGS_URL + str(tag))
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
            sHtmlContent = oRequestHandler.request()

            content = json.loads(sHtmlContent)

            sTitle = content['name'].encode('utf-8')
            sUrl2 = QUALITE_URL + str(tag)
#             sUrl2 = content['link']

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
             
            oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', 'genres.png', '', oOutputParameterHandler)
        progress_.VSclose(progress_)
        
        if total > 0:
            numPage = eval(str(numPage)) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('numPage', numPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
    
# def __checkForNextPage(sHtmlContent):
#     oParser = cParser()
#     sPattern = 'href="([^"]+)"><span class="fa fa-arrow-right">'
#     aResult = oParser.parse(sHtmlContent, sPattern)
#     if (aResult[0] == True):
#         nextPage = aResult[1][0]
#         if not nextPage.startswith('https'):
#             nextPage = URL_MAIN[:-1] + nextPage
#         return nextPage
#     return False

def showMoviesLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    #Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour ce film :[/COLOR]')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()
    
    contents = json.loads(sHtmlContent)

    if contents:
        progress_ = progress().VScreate(SITE_NAME)
        total = len(contents)
        for content in contents:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle = content['title']['rendered'].encode('utf-8')
            sTitle = sTitle.replace('&#8211; Qualité ','[').replace(' | ','](') + ')'
            sUrl2 = POST_URL + str(content['id'])
    
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
             
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', 'genres.png', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')
    sDesc=oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'bold;color:.+?\">(.+?)<.+?action=[^"]"(.+?)[^"]".+?value=[^"]"(.+?)[^"]">.+?value=[^"]"(.+?)[^"]">.+?submit[^"]">(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            # Exclure les fichiers en plusieurs parties ou non identifié comme film 
            DL = aEntry[4]
            if DL != 'T\\u00e9l\\u00e9charger':
                continue

            sHoster = aEntry[0]
            
            oHoster = cHosterGui().checkHoster(sHoster.lower())
            if not oHoster:
                continue

            sUrl2 = aEntry[1]
            encodeData = urllib.quote_plus(aEntry[2])
            data = aEntry[3]
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHoster)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('baseUrl', sUrl)
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('encodeData', encodeData)
            oOutputParameterHandler.addParameter('data', data)
            oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def Display_protected_link():

    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    baseUrl = oInputParameterHandler.getValue('baseUrl')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    encodeData = oInputParameterHandler.getValue('encodeData')
    data = oInputParameterHandler.getValue('data')

    if 'protect-stream' in sUrl:
        f = { 'url' : encodeData, 'nextURL' : data, 'zt' : 'true'}
        data = urllib.urlencode(f)
        sHtmlContent = DecryptDlProtecte(sUrl, data, baseUrl)

        if sHtmlContent:
            print(sHtmlContent)
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = '<div class="lienet"><a href="([^"]+)"'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            dialog().VSok('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    #Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotecte = (True, [sUrl])

    if (aResult_dlprotecte[0]):

        episode = 1

        for aEntry in aResult_dlprotecte[1]:
            sHosterUrl = aEntry

            sTitle = sMovieTitle
            if len(aResult_dlprotecte[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + episode

            episode+= 1

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = 'Qualit.+?galement disponibles pour cette saison:</span><br>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''

def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '"otherversionsspan">Saisons.+?galement disponibles pour cette série:(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    return ''

def DecryptDlProtecte(url, data, baseUrl):

    if not (url):
        return ''

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('Host', url.split('/')[2])
    oRequestHandler.addHeaderEntry('Referer', baseUrl)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
    oRequestHandler.addHeaderEntry('Content-Type',  "application/x-www-form-urlencoded")
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()

    return sHtmlContent

