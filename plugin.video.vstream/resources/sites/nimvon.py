#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Kepliz @fredterros
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.lib.comaddon import progress, VSlog #import du dialog progress
from resources.lib.util import cUtil
import re, unicodedata, urllib, urllib2

URL_HOST = 'http://www.wonior.com/' #TOUT OK
#URL_HOST = 'http://www.bofiaz.com/' #TOUT OK
#URL_HOST = 'http://radego.com'#rradego/' #PLANTE au deuxième lien
#URL_HOST = 'http://www.trozam.com/' #TOUT OK
#URL_HOST = 'http://www.sajbo.com/' #TOUT OK
#URL_HOST = 'http://www.nimvon.com/' #TOUT OK

def sLinkdyn(): #Recherche de la partie dynamyque
    #oGui = cGui()
    oParser4 = cParser()
    
    sPattern4 = 'href="([^"]+)"'
    sUrl4 = URL_HOST 
    
    oRequestHandler4 = cRequestHandler(sUrl4)
    sHtmlContent4 = oRequestHandler4.request()
    
    sPattern5 = '<center>(.+?)</center>'
    sPattern6 = 'window.location.href="(.+?)"'
    
    aResult4 = oParser4.parse(sHtmlContent4, sPattern4)
    aResult5 = oParser4.parse(sHtmlContent4, sPattern5)
    aResult6 = oParser4.parse(sHtmlContent4, sPattern6)
    
    if (aResult6[0] == False):
    
        if (aResult5[0] == True):

            if (aResult4[0] == True):
            
                if (aResult4[1][0].startswith('/') == False):
                    return URL_HOST + aResult4[1][0] + '/'
                else:
                    return URL_HOST + aResult4[1][1] + '/'
                
            else:
                return URL_HOST
                
        else:
            return URL_HOST
    
    else:
        return URL_HOST + aResult6[1][0] + '/'

#from resources.lib.util import cUtil #outils pouvant etre utiles
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
headers = {'User-Agent': UA}
#Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous xbmc

SITE_IDENTIFIER = 'kepliz_com' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = 'Kepliz' #nom que xbmc affiche
SITE_DESC = 'Clear & Simply' #description courte de votre source

#URL_MAIN = 'http://nimvon.com/'
URL_MAIN = sLinkdyn()
#URL_MAIN = 'http://nimvon.com/' #url de votre source

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
URL_SEARCH = (URL_MAIN + 'index.php?ordering=&searchphrase=all&Itemid=9&option=com_search&searchword=', 'showMovies')
#recherche global films
#URL_SEARCH = (URL_MAIN + '?keyword=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'
# menu films existant dans l'acceuil (Home)
MOVIE_NEWS = (URL_MAIN + '', 'showMovies') #films (derniers ajouts = trie par date)
MOVIE_MOVIE = (URL_MAIN + 'index.php', 'showMovies') #films (load source)
#MOVIE_HD = (URL_MAIN + 'url', 'showMovies') #films HD
MOVIE_VIEWS = (URL_MAIN + 'index.php?option=com_content&view=category&id=29&Itemid=8', 'showMovies') #films (les plus vus = populaire)
#MOVIE_COMMENTS = (URL_MAIN + 'url', 'showMovies') #films (les plus commentés) (pas afficher sur HOME)
#MOVIE_GENRES = (URL_MAIN + 'index.php?option=com_content&view=section&id=1&Itemid=6', 'showGenres') #films (les mieux notés)
MOVIE_GENRES = (True, 'showGenres') #films genres
#MOVIE_ANNEES = (True, 'showMovieYears') #films (par années)
#menu supplementaire non gerer par l'acceuil
#MOVIE_VF = (URL_MAIN + 'url', 'showMovies') #films VF
#MOVIE_VOSTFR = (URL_MAIN + 'url', 'showMovies') #films VOSTFR

ANIM_ANIMS = (URL_MAIN + 'index.php?option=com_content&view=category&id=2&Itemid=2', 'showMovies') #animés (load source)

SPORT_SPORTS = (URL_MAIN + 'index.php?option=com_content&view=category&id=26&Itemid=4', 'showMovies') #Documentaire

SERIE_SERIES = (URL_MAIN + 'index.php?option=com_content&view=category&id=3&Itemid=4', 'showMovies') #Séctacles

def load(): #fonction chargee automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage
    
    #oGui.addText(SITE_IDENTIFIER, URL_MAIN)
    
    oOutputParameterHandler = cOutputParameterHandler() #appelle la fonction pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN) # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Catégories', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (A l\'affiche)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés (Tous)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Documentaires (tous)', 'notes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Spéctacles (tous)', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() #ferme l'affichage

def showSearch(): #fonction de recherche
    oGui = cGui()

    sSearchText = oGui.showKeyBoard() #appelle le clavier xbmc
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText#modifie l'url de recherche
        showMovies(sUrl) #appelle la fonction qui pourra lire la page de resultats
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    liste = []
    liste.append( ['Action', URL_MAIN + 'index.php?option=com_content&view=category&id=1:action-&Itemid=14&layout=default'] )
    liste.append( ['Aventure', URL_MAIN + 'index.php?option=com_content&view=category&id=4:aventure-&Itemid=15&layout=default'] )
    liste.append( ['Comédie', URL_MAIN + 'index.php?option=com_content&view=category&id=6:comedie-&Itemid=16&layout=default'] )
    liste.append( ['Drame', URL_MAIN + 'index.php?option=com_content&view=category&id=7:drame-&Itemid=17&layout=default'] )
    liste.append( ['Fantastic', URL_MAIN + 'index.php?option=com_content&view=category&id=8:fantastique-&Itemid=18&layout=default'] )
    liste.append( ['Horreur', URL_MAIN + 'index.php?option=com_content&view=category&id=9:horreur-&Itemid=19&layout=default'] )
    liste.append( ['Policier', URL_MAIN + 'index.php?option=com_content&view=category&id=10:policier-&Itemid=20&layout=default'] )
    liste.append( ['Science fiction', URL_MAIN + 'index.php?option=com_content&view=category&id=11:science-fiction-&Itemid=21&layout=default'] )
    liste.append( ['Thriller', URL_MAIN + 'index.php?option=com_content&view=category&id=12:thriller-&Itemid=22&layout=default'] )
    
    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl) #sortie de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def serchLink2(uUrl):
    #oGui = cGui()
    oParser5 = cParser()
    
    sPattern5 = '<a onclick="window.location.href=\'(.+?)\''
    sUrl5 = uUrl 
    
    oRequestHandler5 = cRequestHandler(sUrl5)
    sHtmlContent5 = oRequestHandler5.request()
    
    aResult5 = oParser5.parse(sHtmlContent5, sPattern5)
    
    if (aResult5[0] == True):
        return aResult5[1][0]
    else:
        return URL_HOST


def showMovies(sSearch=''):
    oGui = cGui() #ouvre l'affichage
    oParser = cParser()
        
    if (sSearch != ''):
        
        if (' ' in sSearch):
            sUrl =  sSearch.replace(' ', '+')
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return            
        else:
            sUrl =  sSearch
            sPattern = '<li>.+?<a href="([^"]+)".+?>(.+?)<font color=".+?">'
            
    else:  
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sTitle2 = oInputParameterHandler.getValue('sMovieTitle')
        
        if ('view=article&id=' in sUrl):
            sPattern = '<iframe src="([^"]+)"'
        elif ('id1=&id2=' in sUrl):
            sPattern = '<a onclick="window.location.href=\'(.+?)\''
        else:
            sPattern = '<a href="([^"]+)">([^<]+)<font color=".+?"><i>.+?</i></font></a>'
        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent=sHtmlContent.replace('<a href="#form1"','')
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER, 'Aucun Résultats')
    
    if (aResult[0] == True):
        progress_ = progress().VScreate(SITE_NAME)
        total = len(aResult[1])
        
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) #dialog update
            if progress_.iscanceled():
                break
            
            if ('<img style' in aEntry[1]):
                continue
            
            if ('view=article&id=' in sUrl):
                sQual = 'HD'      
                sUrl2 = aResult[1][0]
                sTitle = sTitle2                
                sThumb = ''
                sDesc = ''
                sUrl3 = serchLink2(sUrl2)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl3) #sortie de l'url
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                #oGui.addText(SITE_IDENTIFIER, sUrl2)
                #oGui.addText(SITE_IDENTIFIER, 'IF')
            elif ('id1=&id2=' in sUrl):
                sQual = 'HD'      
                sUrl2 = aResult[1][0].replace(';','&')
                sTitle = sTitle2                
                sTitle3 = sTitle2
                sThumb = ''
                sDesc = ''
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2) #sortie de l'url
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                #oGui.addText(SITE_IDENTIFIER, sUrl2)
            else:
                sQual = 'HD'      
                sTitle = aEntry[1]
                sUrl2 = URL_HOST[:-1] + aEntry[0]
                sThumb = ''
                sDesc = ''
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
                oGui.addMovie(SITE_IDENTIFIER, 'showMovies', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                #oGui.addText(SITE_IDENTIFIER, sUrl2)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent) #cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory() #ferme l'affichage
        

def __checkForNextPage(sHtmlContent): #cherche la page suivante
    oParser = cParser()
    sPattern = 'href="([^"]+)" title="Suivant"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return URL_MAIN[:-1] + aResult[1][0]

    return False
            

def showHosters(): #recherche et affiche les hotes
    oGui = cGui() #ouvre l'affichage
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de parametre
    sUrl = oInputParameterHandler.getValue('siteUrl') #apelle siteUrl
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #appelle le titre
    sThumb = oInputParameterHandler.getValue('sThumb') #appelle le poster
    oRequestHandler = cRequestHandler(sUrl) #requete sur l'url
    sHtmlContent = oRequestHandler.request() #requete sur l'url
    oParser = cParser()
    #sPattern = 'file:"([^"]+)'
    sPattern = 'file:"([^"]+)".+?label:"([^"]+)".+?'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            #oGui.addText(SITE_IDENTIFIER, 'Qualité: SD : entre 360p et 720p')
            sHosterUrl = aEntry[0]
            sQual = aEntry[1]
            #oGui.addText(SITE_IDENTIFIER, aEntry[0] + ' - ' + aEntry[1])
            sTitle = sMovieTitle + ' [' + sQual + ']'
            oHoster = cHosterGui().checkHoster(sHosterUrl) #recherche l'hote dans l'addon
            if (oHoster != False):
                oHoster.setDisplayName(sTitle) #nom affiche
                oHoster.setFileName(sMovieTitle) #idem
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            else:
               oGui.addText(SITE_IDENTIFIER, sHosterUrl)
                
    else:            
        oGui.addText(SITE_IDENTIFIER, 'Nothing')       
        
    oGui.setEndOfDirectory()
    #fin