#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog, VSlog
from resources.lib.config import GestionCookie

import re, random
import json

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

MOVIE_GENRES = (URL_MAIN + 'wp-json/wp/v2/categories?per_page=100', 'showGenre')
MOVIE_URL = (URL_MAIN + 'wp-json/wp/v2/posts?per_page=20&categories=')
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

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()
    
    contents = json.loads(sHtmlContent)

    tags = set()

    if contents:
        for content in contents:
            idTag = content['tags']
            tags.add(idTag[0])

        progress_ = progress().VScreate(SITE_NAME)
        total = len(tags)
        for tag in tags:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = TAGS_URL + str(tag)
            oRequestHandler = cRequestHandler(sUrl)
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
            
    oGui.setEndOfDirectory()
    
    
# def showMovies():
#     oGui = cGui()
#     oInputParameterHandler = cInputParameterHandler()
#     sUrl = oInputParameterHandler.getValue('siteUrl')
# 
#     oRequestHandler = cRequestHandler(sUrl)
#     oRequestHandler.addHeaderEntry('User-Agent', UA)
#     oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
#     sHtmlContent = oRequestHandler.request()
#     
#     contents = json.loads(sHtmlContent)
# 
#     if contents:
#         progress_ = progress().VScreate(SITE_NAME)
#         total = len(contents)
#         for content in contents:
#             progress_.VSupdate(progress_, total)
#             if progress_.iscanceled():
#                 break
# 
#             sTitle = content['title']['rendered'].encode('utf-8')
#             sTitle = sTitle.replace('&#8211; Qualité','(') + ')'
#             sUrl2 = POST_URL + str(content['id'])
#    
#             oOutputParameterHandler = cOutputParameterHandler()
#             oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
#             oOutputParameterHandler.addParameter('siteUrl', sUrl2)
#             
#             oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', 'genres.png', '', oOutputParameterHandler)
#         progress_.VSclose(progress_)
# 
#     oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+)"><span class="fa fa-arrow-right">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        nextPage = aResult[1][0]
        if not nextPage.startswith('https'):
            nextPage = URL_MAIN[:-1] + nextPage
        return nextPage
    return False

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
#            sTitle = sTitle.replace('&#8211; Qualité','(') + ')'
            sUrl2 = POST_URL + str(content['id'])
    
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
             
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', 'genres.png', '', oOutputParameterHandler)

#         total = len(contents)
#         progress_ = progress().VScreate(SITE_NAME)
#         progress_.VSupdate(progress_, total)
#         shtml = contents['content']['rendered'].encode('utf-8')
#         oParser = cParser()
# #         sPattern = '<em>=(.+?)</em>'
# #         aResult = oParser.parse(sHtmlContent, sPattern)
# #         sDesc = aResult[1]
#         sPattern = 'href="([^"]+)"'
#         aResult = oParser.parse(shtml, sPattern)
# 
#         for aEntry in aResult[1]:
#             if progress_.iscanceled():
#                 break
#             sUrl2 = aEntry
#    
#             oOutputParameterHandler = cOutputParameterHandler()
#             oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
#             oOutputParameterHandler.addParameter('siteUrl', sUrl2)
#             
#             oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', 'movies.png', '', oOutputParameterHandler)
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
    #sPattern = 'bold;color:.+?\\">(.+?)<\/div><\/b><b><form action=[^"]"(.+?)[^"]"'
    sPattern = 'bold;color:.+?\\">(.+?)<\/div><\/b><b><form action=[^"]"(.+?)[^"]".+?submit[^"]">(.+?)<'
#     sPattern = 'target=\"_blank\">([^"]+)</a></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            # Exclure les fichiers en plusieurs parties
            DL = aEntry[2]
            if DL != 'T\\u00e9l\\u00e9charger':
                continue

            sHoster = aEntry[0]
            sUrl2 = aEntry[1]
            # sHoster = aEntry[0]
#             sHoster = re.sub('\.\w+', '', aEntry)
#             sUrl2 = URL_MAIN[:-1] + aEntry[1]
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHoster)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()



def Display_protected_link():
    #VSlog('Display_protected_link')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'link' in sUrl:
        #Temporairement car la flemme de ce battre avec les redirection
        import requests
        headers = {'User-Agent': UA}
        r = requests.get(sUrl.replace('//link', '/link'), headers = headers)
        sUrl = r.url

    if "dl-protect" in sUrl:
        sHtmlContent = DecryptDlProtecte(sUrl)

        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = '<div class="lienet"><a href="(.+?)">'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            oDialog = dialog().VSok('Erreur décryptage du lien')
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

def DecryptDlProtecte(url):
    VSlog('DecryptDlProtecte : ' + url)

    if not (url):
        return ''

    # 1ere Requete pour recuperer le cookie
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)

    cookies = GestionCookie().Readcookie('www_dl-protect1_co')
    #VSlog( 'cookie'  + str(cookies))

    #Tout ca a virer et utiliser oRequestHandler.addMultipartFiled('sess_id': sId, 'upload_type': 'url', 'srv_tmp_url': sTmp) quand ca marchera
    import string
    _BOUNDARY_CHARS = string.digits
    boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(29))
    multipart_form_data = {'submit': 'continuer', 'submit': 'Continuer'}
    data, headersMulti = encode_multipart(multipart_form_data, {}, boundary)

    #2 eme requete pour avoir le lien
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('Host', url.split('/')[2])
    oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Content-Length', headersMulti['Content-Length'])
    oRequestHandler.addHeaderEntry('Content-Type', headersMulti['Content-Type'])
    oRequestHandler.addHeaderEntry('Cookie', cookies)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')

    oRequestHandler.addParametersLine(data)

    sHtmlContent = oRequestHandler.request()

    #fh = open('d:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    return sHtmlContent

#******************************************************************************
#from http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/

"""Encode multipart form data to upload files via POST."""

def encode_multipart(fields, files, boundary = None):
    r"""Encode dict of form fields and dict of files as multipart/form-data.
    Return tuple of (body_string, headers_dict). Each value in files is a dict
    with required keys 'filename' and 'content', and optional 'mimetype' (if
    not specified, tries to guess mime type or uses 'application/octet-stream').

    >>> body, headers = encode_multipart({'FIELD': 'VALUE'},
    ...                                  {'FILE': {'filename': 'F.TXT', 'content': 'CONTENT'}},
    ...                                  boundary='BOUNDARY')
    >>> print('\n'.join(repr(l) for l in body.split('\r\n')))
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FIELD"'
    ''
    'VALUE'
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FILE"; filename="F.TXT"'
    'Content-Type: text/plain'
    ''
    'CONTENT'
    '--BOUNDARY--'
    ''
    >>> print(sorted(headers.items()))
    [('Content-Length', '193'), ('Content-Type', 'multipart/form-data; boundary=BOUNDARY')]
    >>> len(body)
    193
    """

    import mimetypes
    import string

    _BOUNDARY_CHARS = string.digits

    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(29))

    lines = []

    for name, value in fields.items():
        lines.extend((
            '-----------------------------{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
            '',
            str(value),
            '-----------------------------{0}--'.format(boundary),
            '',
        ))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(
                    escape_quote(name), escape_quote(filename)),
            'Content-Type: {0}'.format(mimetype),
            '',
            value['content'],
        ))

    body = '\r\n'.join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary=---------------------------{0}'.format(boundary),
        'Content-Length': str(len(body)),
    }

    return (body, headers)
