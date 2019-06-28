# -*- coding: utf-8 -*-
"""
Unit tests for the htmldate library.
"""
# https://docs.pytest.org/en/latest/

import logging
import os
import re
import sys

import dateparser

from htmldate.core import *
from htmldate import cli, utils


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

MOCK_PAGES = { \
'http://blog.python.org/2016/12/python-360-is-now-available.html': 'blog.python.org.html', \
'https://example.com': 'example.com.html', \
'https://github.com/adbar/htmldate': 'github.com.html', \
'https://creativecommons.org/about/': 'creativecommons.org.html', \
'https://en.support.wordpress.com/': 'support.wordpress.com.html', \
'https://en.blog.wordpress.com/': 'blog.wordpress.com.html', \
'https://www.deutschland.de/en': 'deutschland.de.en.html', \
'https://www.gnu.org/licenses/gpl-3.0.en.html': 'gnu.org.gpl.html', \
'https://opensource.org/': 'opensource.org.html', \
'https://www.austria.info/': 'austria.info.html', \
'https://www.portal.uni-koeln.de/9015.html?&L=1&tx_news_pi1%5Bnews%5D=4621&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Baction%5D=detail&cHash=7bc78dfe3712855026fc717c2ea8e0d3': 'uni-koeln.de.ocean.html', \
'https://www.intel.com/content/www/us/en/legal/terms-of-use.html': 'intel.com.tos.html', \
'http://www.greenpeace.org/international/en/campaigns/forests/asia-pacific/': 'greenpeace.org.forests.html', \
'https://www.amnesty.org/en/what-we-do/corporate-accountability/': 'amnesty.org.corporate.html', \
'http://www.medef.com/en/content/alternative-dispute-resolution-for-antitrust-damages': 'medef.fr.dispute.html', \
'https://www.rosneft.com/business/Upstream/Licensing/': 'rosneft.com.licensing.html', \
'https://www.creativecommons.at/faircoin-hackathon': 'creativecommons.at.faircoin.html', \
'https://pixabay.com/en/service/terms/': 'pixabay.com.tos.html', \
'https://futurezone.at/digital-life/wie-creativecommons-richtig-genutzt-wird/24.600.504': 'futurezone.at.cc.html', \
'https://500px.com/photo/26034451/spring-in-china-by-alexey-kruglov': '500px.com.spring.html', \
'https://www.eff.org/files/annual-report/2015/index.html': 'eff.org.2015.html', \
'http://unexpecteduser.blogspot.de/2011/': 'unexpecteduser.2011.html', \
'https://bayern.de/': 'bayern.de.html', \
'https://www.facebook.com/visitaustria/': 'facebook.com.visitaustria.html', \
'http://www.stuttgart.de/': 'stuttgart.de.html', \
'https://www.gruene-niedersachsen.de': 'gruene-niedersachsen.de.html', \
'https://die-partei.net/sh/': 'die-partei.net.sh.html', \
'https://www.pferde-fuer-unsere-kinder.de/unsere-projekte/': 'pferde.projekte.de.html', \
'http://www.hundeverein-kreisunna.de/termine.html': 'hundeverein-kreisunna.de.html', \
'http://www.hundeverein-querfurt.de/index.php?option=com_content&view=article&id=54&Itemid=50': 'hundeverein-querfurt.de.html', \
'http://absegler.de/': 'absegler.de.html', \
'http://viehbacher.com/de/spezialisierung/internationale-forderungsbeitreibung': 'viehbacher.com.forderungsbetreibung.html', \
'http://www.jovelstefan.de/2012/05/11/parken-in-paris/': 'jovelstefan.de.parken.html', \
'http://www.freundeskreis-videoclips.de/waehlen-sie-car-player-tipps-zur-auswahl-der-besten-car-cd-player/': 'freundeskreis-videoclips.de.html', \
'https://www.scs78.de/news/items/warm-war-es-schoen-war-es.html': 'scs78.de.html', \
'https://www.goodform.ch/blog/schattiges_plaetzchen': 'goodform.ch.blog.html', \
'https://www.transgen.de/aktuell/2687.afrikanische-schweinepest-genome-editing.html': 'transgen.de.aktuell.html', \
'http://www.eza.gv.at/das-ministerium/presse/aussendungen/2018/07/aussenministerin-karin-kneissl-beim-treffen-der-deutschsprachigen-aussenminister-in-luxemburg/': 'eza.gv.at.html', \
'https://aboutpam.com/fitness/the-%22right%22-diet-what-does-that-even-mean': 'aboutpam.com.html', \
'https://www.horizont.net/marketing/kommentare/influencer-marketing-was-sich-nach-dem-vreni-frost-urteil-aendert-und-aendern-muss-172529': 'horizont.net.html', \
'http://www.klimawandel-global.de/klimaschutz/energie-sparen/elektromobilitat-der-neue-trend/': 'klimawandel-global.de.html', \
'http://blog.kinra.de/?p=959/': 'kinra.de.html', \
'http://www.hobby-werkstatt-blog.de/arduino/424-eine-arduino-virtual-wall-fuer-den-irobot-roomba.php': 'hobby-werkstatt-blog.de.roomba.html', \
'https://www.tagesausblick.de/Analyse/USA/DOW-Jones-Jahresendrally-ade__601.html': 'tagesausblick.de.dow.html', \
'http://www.heimicke.de/chronik/zahlen-und-daten/': 'heimicke.de.zahlen.html', \
'https://www.weltwoche.ch/ausgaben/2019-4/artikel/forbes-die-weltwoche-ausgabe-4-2019.html': 'weltwoche.ch.html', \
'http://blog.todamax.net/2018/midp-emulator-kemulator-und-brick-challenge/': 'blog.todamax.net.html', \
'https://www.channelpartner.de/a/sieben-berufe-die-zukunft-haben,3050673': 'channelpartner.de.berufe.html', \
'https://www.beltz.de/fachmedien/paedagogik/didacta_2019_in_koeln_19_23_februar/beltz_veranstaltungen_didacta_2016/veranstaltung.html?tx_news_pi1%5Bnews%5D=14392&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Baction%5D=detail&cHash=10b1a32fb5b2b05360bdac257b01c8fa': 'beltz.de.didakta.html', \
'http://www.pbrunst.de/news/2011/12/kein-cyberterrorismus-diesmal/': 'pbrunst.de.html', \
}
# '': '', \


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUTFORMAT = '%Y-%m-%d'
# PARSER = dateparser.DateDataParser(settings={'PREFER_DAY_OF_MONTH': 'first', 'PREFER_DATES_FROM': 'past', 'DATE_ORDER': 'DMY'})
PARSER = dateparser.DateDataParser(languages=['de', 'en'], settings={'PREFER_DAY_OF_MONTH': 'first', 'PREFER_DATES_FROM': 'past', 'DATE_ORDER': 'DMY'}) # allow_redetect_language=False,


def load_mock_page(url):
    '''load mock page from samples'''
    with open(os.path.join(TEST_DIR, 'cache', MOCK_PAGES[url]), 'r') as inputf:
        htmlstring = inputf.read()
    return htmlstring


def test_input():
    '''test if loaded strings/trees are handled properly'''
    assert load_html(123) == (None, None)
    assert load_html('<html><body>XYZ</body></html>') is not None
    assert find_date(None) is None


def test_no_date():
    '''these pages should not return any date'''
    assert find_date(load_mock_page('https://example.com')) is None
    assert find_date(load_mock_page('https://www.intel.com/content/www/us/en/legal/terms-of-use.html')) is None
    # safe search
    assert find_date(load_mock_page('https://en.support.wordpress.com/'), False) is None
    assert find_date(load_mock_page('https://en.support.wordpress.com/')) is None
    # errors
    assert find_date(' ', outputformat='X%') is None
    assert find_date('<html></html>', outputformat='%X') is None
    assert find_date('<html></html>', url='http://www.website.com/9999/01/43/') is None
    assert find_date('<html></html>', url='http://www.website.com/9999/01/43/') is None


def test_exact_date():
    '''these pages should return an exact date'''
    ## HTML tree
    assert find_date('<html><head><meta property="dc:created" content="2017-09-01"/></head><body></body></html>') == '2017-09-01'
    assert find_date('<html><head><meta property="OG:Updated_Time" content="2017-09-01"/></head><body></body></html>') == '2017-09-01'
    assert find_date('<html><head><meta name="created" content="2017-01-09"/></head><body></body></html>') == '2017-01-09'
    assert find_date('<html><head><meta itemprop="copyrightyear" content="2017"/></head><body></body></html>') == '2017-01-01'
    assert find_date('<html><body><span class="entry-date">July 12th, 2016</span></body></html>') == '2016-07-12'

    ## link in header
    assert find_date(load_mock_page('http://www.jovelstefan.de/2012/05/11/parken-in-paris/')) == '2012-05-11'

    ## meta in header
    assert find_date('<html><head><meta/></head><body></body></html>') is None
    assert find_date(load_mock_page('http://blog.python.org/2016/12/python-360-is-now-available.html')) == '2016-12-23'
    assert find_date(load_mock_page('https://500px.com/photo/26034451/spring-in-china-by-alexey-kruglov')) == '2013-02-16'
    assert find_date('<html><head><meta name="og:url" content="http://www.example.com/2018/02/01/entrytitle"/></head><body></body></html>') == '2018-02-01'
    assert find_date('<html><head><meta itemprop="datecreated" datetime="2018-02-02"/></head><body></body></html>') == '2018-02-02'
    assert find_date('<html><head><meta itemprop="datemodified" content="2018-02-04"/></head><body></body></html>') == '2018-02-04'
    assert find_date('<html><head><meta http-equiv="last-modified" content="2018-02-05"/></head><body></body></html>') == '2018-02-05'
    assert find_date('<html><head><meta name="Publish_Date" content="02.02.2004"/></head><body></body></html>') == '2004-02-02'
    assert find_date('<html><head><meta name="pubDate" content="2018-02-06"/></head><body></body></html>') == '2018-02-06'
    assert find_date('<html><head><meta pubdate="pubDate" content="2018-02-06"/></head><body></body></html>') == '2018-02-06'
    assert find_date('<html><head><meta itemprop="DateModified" datetime="2018-02-06"/></head><body></body></html>') == '2018-02-06'
    # other format
    assert find_date(load_mock_page('http://blog.python.org/2016/12/python-360-is-now-available.html'), outputformat='%d %B %Y') == '23 December 2016'

    ## time in document body
    assert find_date(load_mock_page('https://www.facebook.com/visitaustria/')) == '2017-10-08'
    assert find_date(load_mock_page('http://absegler.de/')) == '2017-08-06'
    assert find_date(load_mock_page('http://www.medef.com/en/content/alternative-dispute-resolution-for-antitrust-damages')) == '2017-09-01'
    assert find_date('<html><body><time datetime="08:00"></body></html>') is None
    assert find_date('<html><body><time datetime="2014-07-10 08:30:45.687"></body></html>') == '2014-07-10'
    assert find_date('<html><head></head><body><time class="entry-time" itemprop="datePublished" datetime="2018-04-18T09:57:38+00:00"></body></html>') == '2018-04-18'
    assert find_date('<html><body><footer class="article-footer"><p class="byline">Veröffentlicht am <time class="updated" datetime="2019-01-03T14:56:51+00:00">3. Januar 2019 um 14:56 Uhr.</time></p></footer></body></html>') == '2019-01-03'
    assert find_date('<html><body><footer class="article-footer"><p class="byline">Veröffentlicht am <time class="updated" datetime="2019-01-03T14:56:51+00:00"></time></p></footer></body></html>') == '2019-01-03'

    ## precise pattern in document body
    assert find_date('<html><body><font size="2" face="Arial,Geneva,Helvetica">Bei <a href="../../sonstiges/anfrage.php"><b>Bestellungen</b></a> bitte Angabe der Titelnummer nicht vergessen!<br><br>Stand: 03.04.2019</font></body></html>') == '2019-04-03'
    assert find_date('<html><body>Datum: 10.11.2017</body></html>') == '2017-11-10'
    assert find_date(load_mock_page('https://www.tagesausblick.de/Analyse/USA/DOW-Jones-Jahresendrally-ade__601.html')) == '2012-12-22'
    assert find_date(load_mock_page('http://blog.todamax.net/2018/midp-emulator-kemulator-und-brick-challenge/')) == '2018-02-15'
    assert find_date(load_mock_page('https://www.channelpartner.de/a/sieben-berufe-die-zukunft-haben,3050673')) == '2019-04-03' # JSON dateModified

    ## meta in document body
    assert find_date(load_mock_page('https://futurezone.at/digital-life/wie-creativecommons-richtig-genutzt-wird/24.600.504')) == '2013-08-09'
    assert find_date(load_mock_page('https://aboutpam.com/fitness/the-%22right%22-diet-what-does-that-even-mean')) == '2017-12-15'
    assert find_date(load_mock_page('https://www.horizont.net/marketing/kommentare/influencer-marketing-was-sich-nach-dem-vreni-frost-urteil-aendert-und-aendern-muss-172529')) == '2019-01-29'
    assert find_date(load_mock_page('http://www.klimawandel-global.de/klimaschutz/energie-sparen/elektromobilitat-der-neue-trend/')) == '2013-05-03'
    assert find_date(load_mock_page('http://www.hobby-werkstatt-blog.de/arduino/424-eine-arduino-virtual-wall-fuer-den-irobot-roomba.php')) == '2015-12-14'
    assert find_date(load_mock_page('https://www.beltz.de/fachmedien/paedagogik/didacta_2019_in_koeln_19_23_februar/beltz_veranstaltungen_didacta_2016/veranstaltung.html?tx_news_pi1%5Bnews%5D=14392&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Baction%5D=detail&cHash=10b1a32fb5b2b05360bdac257b01c8fa')) == '2019-02-20'
    # does not work
    # assert find_date('<html><body><span class="date">Mai<span>06</span>2018</span></body></html>') == '2018-05-06' # https://www.wienbadminton.at/news/119843/Come-Together

    # abbr in document body
    assert find_date(load_mock_page('http://blog.kinra.de/?p=959/')) == '2012-12-16'
    assert find_date('<html><body><abbr class="published">am 12.11.16</abbr></body></html>') == '2016-11-12'
    assert find_date('<html><body><abbr class="date-published">8.11.2016</abbr></body></html>') == '2016-11-08'
    # valid vs. invalid data-utime
    assert find_date('<html><body><abbr data-utime="1438091078" class="something">A date</abbr></body></html>') == '2015-07-28'
    assert find_date('<html><body><abbr data-utime="143809-1078" class="something">A date</abbr></body></html>') is None
    # other format
    assert find_date(load_mock_page('https://futurezone.at/digital-life/wie-creativecommons-richtig-genutzt-wird/24.600.504'), outputformat='%d %B %Y') == '09 August 2013'

    ## other expressions in document body
    assert find_date('<html><body>"datePublished":"2018-01-04"</body></html>') == '2018-01-04'
    assert find_date('<html><body><time>2018-01-04</time></body></html>') == '2018-01-04'
    assert find_date('<html><body>Stand: 1.4.18</body></html>') == '2018-04-01'
    assert find_date(load_mock_page('http://www.stuttgart.de/')) == '2017-10-09'

    ## in document body
    assert find_date(load_mock_page('https://github.com/adbar/htmldate')) == '2017-08-25'
    assert find_date(load_mock_page('https://en.blog.wordpress.com/')) == '2017-08-30'
    assert find_date(load_mock_page('https://www.gnu.org/licenses/gpl-3.0.en.html')) == '2016-11-18'
    assert find_date(load_mock_page('https://opensource.org/')) == '2017-09-05'
    assert find_date(load_mock_page('https://www.austria.info/')) == '2017-09-07'
    assert find_date(load_mock_page('https://www.portal.uni-koeln.de/9015.html?&L=1&tx_news_pi1%5Bnews%5D=4621&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Baction%5D=detail&cHash=7bc78dfe3712855026fc717c2ea8e0d3')) == '2017-07-12'
    assert find_date(load_mock_page('https://www.eff.org/files/annual-report/2015/index.html')) == '2016-05-04'
    assert find_date(load_mock_page('http://unexpecteduser.blogspot.de/2011/')) == '2011-03-30'
    assert find_date(load_mock_page('https://www.gruene-niedersachsen.de')) == '2017-10-09'
    assert find_date(load_mock_page('https://die-partei.net/sh/')) == '2014-07-19'
    assert find_date(load_mock_page('https://www.rosneft.com/business/Upstream/Licensing/')) == '2017-02-27' # most probably 2014-12-31, found in text
    assert find_date(load_mock_page('http://www.freundeskreis-videoclips.de/waehlen-sie-car-player-tipps-zur-auswahl-der-besten-car-cd-player/')) == '2017-07-12'
    assert find_date(load_mock_page('https://www.scs78.de/news/items/warm-war-es-schoen-war-es.html')) == '2018-06-10'
    assert find_date(load_mock_page('https://www.goodform.ch/blog/schattiges_plaetzchen')) == '2018-06-27'
    assert find_date(load_mock_page('https://www.transgen.de/aktuell/2687.afrikanische-schweinepest-genome-editing.html')) == '2018-01-18'
    assert find_date(load_mock_page('http://www.eza.gv.at/das-ministerium/presse/aussendungen/2018/07/aussenministerin-karin-kneissl-beim-treffen-der-deutschsprachigen-aussenminister-in-luxemburg/')) == '2018-07-03'
    assert find_date(load_mock_page('https://www.weltwoche.ch/ausgaben/2019-4/artikel/forbes-die-weltwoche-ausgabe-4-2019.html')) == '2019-01-23'
    # other format
    assert find_date(load_mock_page('http://unexpecteduser.blogspot.de/2011/'), outputformat='%d %B %Y') == '30 March 2011'
    # free text
    assert find_date('<html><body>&copy; 2017</body></html>') == '2017-01-01'
    assert find_date('<html><body>© 2017</body></html>') == '2017-01-01'
    assert find_date('<html><body><p>Dieses Datum ist leider ungültig: 30. Februar 2018.</p></body></html>', extensive_search=False) is None


def test_approximate_date():
    '''this page should return an approximate date'''
    # copyright text
    assert find_date(load_mock_page('http://viehbacher.com/de/spezialisierung/internationale-forderungsbeitreibung')) == '2016-01-01' # somewhere in 2016
    # other
    assert find_date(load_mock_page('https://creativecommons.org/about/')) == '2017-08-11' # or '2017-08-03'
    assert find_date(load_mock_page('https://www.deutschland.de/en')) == '2017-08-01' # or?
    assert find_date(load_mock_page('http://www.greenpeace.org/international/en/campaigns/forests/asia-pacific/')) == '2017-04-28'
    assert find_date(load_mock_page('https://www.amnesty.org/en/what-we-do/corporate-accountability/')) == '2017-07-01'
    assert find_date(load_mock_page('https://www.creativecommons.at/faircoin-hackathon')) == '2017-07-24'
    assert find_date(load_mock_page('https://pixabay.com/en/service/terms/')) == '2017-01-01' # actually 2017-08-09
    assert find_date(load_mock_page('https://bayern.de/')) == '2017-10-06' # most probably 2017-10-06
    assert find_date(load_mock_page('https://www.pferde-fuer-unsere-kinder.de/unsere-projekte/')) == '2016-07-20' # most probably 2016-07-15
    assert find_date(load_mock_page('http://www.hundeverein-querfurt.de/index.php?option=com_content&view=article&id=54&Itemid=50')) == '2016-05-01' # 2010-11-01 in meta, 2016 more plausible
    assert find_date(load_mock_page('http://www.pbrunst.de/news/2011/12/kein-cyberterrorismus-diesmal/')) == '2011-12-01'
    # other format
    assert find_date(load_mock_page('https://www.amnesty.org/en/what-we-do/corporate-accountability/'), outputformat='%d %B %Y') == '01 July 2017'
    # dates in table
    # assert find_date(load_mock_page('http://www.hundeverein-kreisunna.de/termine.html')) == '2017-03-29' # probably newer


def test_date_validator():
    '''test internal date validation'''
    assert date_validator('2016-01-01', OUTPUTFORMAT) is True
    assert date_validator('1998-08-08', OUTPUTFORMAT) is True
    assert date_validator('2001-12-31', OUTPUTFORMAT) is True
    assert date_validator('1992-07-30', OUTPUTFORMAT) is False
    assert date_validator('1901-13-98', OUTPUTFORMAT) is False
    assert date_validator('202-01', OUTPUTFORMAT) is False
    assert date_validator('1922', '%Y') is False
    assert date_validator('2004', '%Y') is True


def test_convert_date():
    '''test date conversion'''
    assert convert_date('2016-11-18', '%Y-%m-%d', '%d %B %Y') == '18 November 2016'
    assert convert_date('18 November 2016', '%d %B %Y', '%Y-%m-%d') == '2016-11-18'


def test_output_format_validator():
    '''test internal output format validation'''
    assert output_format_validator('%Y-%m-%d') is True
    assert output_format_validator('%M-%Y') is True
    assert output_format_validator('ABC') is False
    assert output_format_validator(123) is False
    assert output_format_validator('X%') is False


def test_try_ymd_date():
    '''test date extraction via external package'''
    find_date.extensive_search = False
    assert try_ymd_date('Fri, Sept 1, 2017', OUTPUTFORMAT, PARSER) is None
    find_date.extensive_search = True
    assert try_ymd_date('Friday, September 01, 2017', OUTPUTFORMAT, PARSER) == '2017-09-01'
    assert try_ymd_date('Fri, Sept 1, 2017', OUTPUTFORMAT, PARSER) == '2017-09-01'
    assert try_ymd_date('Fr, 1 Sep 2017 16:27:51 MESZ', OUTPUTFORMAT, PARSER) == '2017-09-01'
    assert try_ymd_date('Freitag, 01. September 2017', OUTPUTFORMAT, PARSER) == '2017-09-01'
    # assert try_ymd_date('Am 1. September 2017 um 15:36 Uhr schrieb', OUTPUTFORMAT) == '2017-09-01'
    assert try_ymd_date('1.9.2017', OUTPUTFORMAT, PARSER) == '2017-09-01'
    assert try_ymd_date('1/9/17', OUTPUTFORMAT, PARSER) == '2017-01-09' # assuming MDY format
    assert try_ymd_date('201709011234', OUTPUTFORMAT, PARSER) == '2017-09-01'
    # other output format
    assert try_ymd_date('1.9.2017', '%d %B %Y', PARSER) == '01 September 2017'
    # wrong
    assert try_ymd_date('201', OUTPUTFORMAT, PARSER) is None
    assert try_ymd_date('14:35:10', OUTPUTFORMAT, PARSER) is None
    assert try_ymd_date('12:00 h', OUTPUTFORMAT, PARSER) is None


#def test_header():
#    assert examine_header(tree, OUTPUTFORMAT, PARSER)


def test_compare_reference():
    '''test comparison function'''
    assert compare_reference(0, 'AAAA', OUTPUTFORMAT) == 0
    assert compare_reference(1517500000, '2018-33-01', OUTPUTFORMAT) == 1517500000
    assert 1517400000 < compare_reference(0, '2018-02-01', OUTPUTFORMAT) < 1517500000
    assert compare_reference(1517500000, '2018-02-01', OUTPUTFORMAT) == 1517500000


def test_regex_parse():
    '''test date extraction using rules and regular expressions'''
    assert regex_parse_de('3. Dezember 2008') is not None
    assert regex_parse_de('33. Dezember 2008') is None
    assert regex_parse_en('Tuesday, March 26th, 2019') is not None
    assert regex_parse_en('3rd Tuesday in March') is None
    assert regex_parse_en('3/14/2016') is not None
    assert regex_parse_en('36/14/2016') is None
    assert custom_parse('12122004', OUTPUTFORMAT) is None
    assert custom_parse('20041212', OUTPUTFORMAT) is not None
    assert custom_parse('1212-20-04', OUTPUTFORMAT) is None
    assert custom_parse('2004-12-12', OUTPUTFORMAT) is not None
    assert custom_parse('33.20.2004', OUTPUTFORMAT) is None
    assert custom_parse('12.12.2004', OUTPUTFORMAT) is not None


def test_url():
    '''test url parameter'''
    assert find_date('<html><body><p>Aaa, bbb.</p></body></html>', url='http://example.com/category/2016/07/12/key-words') == '2016-07-12'
    assert find_date('<html><body><p>Aaa, bbb.</p></body></html>', url='http://example.com/2016/key-words') is None
    assert find_date('<html><body><p>Aaa, bbb.</p></body></html>', url='http://www.kreditwesen.org/widerstand-berlin/2012-11-29/keine-kurzung-bei-der-jugend-klubs-konnen-vorerst-aufatmen-bvv-beschliest-haushaltsplan/') == '2012-11-29'
    assert find_date('<html><body><p>Aaa, bbb.</p></body></html>', url='http://www.kreditwesen.org/widerstand-berlin/2012-11/keine-kurzung-bei-der-jugend-klubs-konnen-vorerst-aufatmen-bvv-beschliest-haushaltsplan/') is None
    assert find_date('<html><body><p>Aaa, bbb.</p></body></html>', url='http://www.kreditwesen.org/widerstand-berlin/6666-42-87/') is None
    assert find_date('<html><body><p>Z.</p></body></html>', url='https://www.pamelaandersonfoundation.org/news/2019/6/26/dm4wjh7skxerzzw8qa8cklj8xdri5j') == '2019-06-26'
    assert extract_partial_url_date('https://testsite.org/2018/01/test', '%Y-%m-%d') == '2018-01-01'
    assert extract_partial_url_date('https://testsite.org/2018/33/test', '%Y-%m-%d') is None


def test_approximate_url():
    '''test url parameter'''
    assert find_date('<html><body><p>Aaa, bbb.</p></body></html>', url='http://example.com/blog/2016/07/key-words') == '2016-07-01'
    assert find_date('<html><body><p>Aaa, bbb.</p></body></html>', url='http://example.com/category/2016/') is None


def test_search_pattern():
    '''test pattern search in strings'''
    #
    pattern = re.compile('\D([0-9]{4}[/.-][0-9]{2})\D')
    catch = re.compile('([0-9]{4})[/.-]([0-9]{2})')
    yearpat = re.compile('^([12][0-9]{3})')
    assert search_pattern('It happened on the 202.E.19, the day when it all began.', pattern, catch, yearpat) is None
    assert search_pattern('The date is 2002.02.15.', pattern, catch, yearpat) is not None
    assert search_pattern('http://www.url.net/index.html', pattern, catch, yearpat) is None
    assert search_pattern('http://www.url.net/2016/01/index.html', pattern, catch, yearpat) is not None
    #
    pattern = re.compile('\D([0-9]{2}[/.-][0-9]{4})\D')
    catch = re.compile('([0-9]{2})[/.-]([0-9]{4})')
    yearpat = re.compile('([12][0-9]{3})$')
    assert search_pattern('It happened on the 202.E.19, the day when it all began.', pattern, catch, yearpat) is None
    assert search_pattern('It happened on the 15.02.2002, the day when it all began.', pattern, catch, yearpat) is not None
    #
    pattern = re.compile('\D(2[01][0-9]{2})\D')
    catch = re.compile('(2[01][0-9]{2})')
    yearpat = re.compile('^(2[01][0-9]{2})')
    assert search_pattern('It happened in the film 300.', pattern, catch, yearpat) is None
    assert search_pattern('It happened in 2002.', pattern, catch, yearpat) is not None


def test_search_html():
    '''test pattern search in HTML'''
    # file input
    assert search_page(load_mock_page('https://www.portal.uni-koeln.de/9015.html?&L=1&tx_news_pi1%5Bnews%5D=4621&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Baction%5D=detail&cHash=7bc78dfe3712855026fc717c2ea8e0d3'), OUTPUTFORMAT) == '2017-07-12'
    # file input + output format
    assert search_page(load_mock_page('http://www.heimicke.de/chronik/zahlen-und-daten/'), '%d %B %Y') == '06 April 2019'
    # tree input
    assert search_page('<html><body><p>The date is 5/2010</p></body></html>', OUTPUTFORMAT) == '2010-05-01'
    assert search_page('<html><body><p>The date is 5.5.2010</p></body></html>', OUTPUTFORMAT) == '2010-05-05'
    assert search_page('<html><body><p>The date is 11/10/99</p></body></html>', OUTPUTFORMAT) == '1999-10-11'
    assert search_page('<html><body><p>The date is 3/3/11</p></body></html>', OUTPUTFORMAT) == '2011-03-03'
    assert search_page('<html><body><p>The date is 06.12.06</p></body></html>', OUTPUTFORMAT) == '2006-12-06'
    assert search_page('<html><body><p>The timestamp is 20140915D15:23H</p></body></html>', OUTPUTFORMAT) == '2014-09-15'
    assert search_page('<html><body><p>It could be 2015-04-30 or 2003-11-24.</p></body></html>', OUTPUTFORMAT) == '2015-04-30'
    assert search_page('<html><body><p>It could be 03/03/2077 or 03/03/2013.</p></body></html>', OUTPUTFORMAT) == '2013-03-03'
    assert search_page('<html><body><p>It could not be 03/03/2077 or 03/03/1988.</p></body></html>', OUTPUTFORMAT) is None
    assert search_page('<html><body><p>© The Web Association 2013.</p></body></html>', OUTPUTFORMAT) == '2013-01-01'
    assert search_page('<html><body><p>Next © Copyright 2018</p></body></html>', OUTPUTFORMAT) == '2018-01-01'


def test_cli():
    '''test the command-line interface'''
    assert cli.examine(' ', True) is None
    assert cli.examine('0'*int(10e7), True) is None
    assert cli.examine('<html><body><span class="entry-date">12. Juli 2016</span></body></html>', True) == '2016-07-12'
    assert cli.examine('<html><body>2016-07-12</body></html>', True) == '2016-07-12'


def test_load():
    '''test the download utility'''
    assert utils.fetch_url('https://www.iana.org/404') is None
    assert utils.fetch_url('https://www.google.com/blank.html') is None
    # print(len(download.fetch_url('https://blank.org').text))
    assert utils.load_html('https://example.org/') is not None


def test_download():
    '''test page download'''
    assert utils.fetch_url('https://httpbin.org/status/404') is None
    url = 'https://httpbin.org/status/200'
    teststring = utils.fetch_url(url)
    assert teststring is None
    assert cli.examine(teststring) is None
    url = 'https://httpbin.org/links/2/2'
    teststring = utils.fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring) is None
    url = 'https://httpbin.org/html'
    teststring = utils.fetch_url(url)
    assert teststring is not None
    assert cli.examine(teststring, False) is None


if __name__ == '__main__':

    # meta
    test_output_format_validator()

    # function-level
    test_input()
    test_date_validator()
    test_search_pattern()
    test_try_ymd_date()
    test_convert_date()
    test_compare_reference()
    test_regex_parse()
    #test_header()

    # module-level
    test_no_date()
    test_exact_date()
    test_approximate_date()
    test_search_html()
    test_url()
    test_approximate_url()

    # cli
    test_cli()

    # loading functions
    test_load()
    test_download()
