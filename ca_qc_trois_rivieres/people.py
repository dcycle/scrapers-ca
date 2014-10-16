# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re
import requests

from six.moves.urllib.parse import urljoin

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://laville.v3r.net/portail/index.aspx?sect=0&module=5&module2=1&MenuID=150&CPage=1'

MAYOR_URL = 'http://laville.v3r.net/portail/index.aspx?sect=0&module=5&module2=1&MenuID=1&CPage=1'


class TroisRivieresPersonScraper(Scraper):

  def scrape(self):
    # mayor first, can't find email
    page = lxmlize(MAYOR_URL)
    photo_url = page.xpath('string(//img/@src[contains(., "Maire")])')
    name = page.xpath('string(//td[@class="contenu"]/text()[last()])')
    p = Person(name=name, district="Trois-Rivières", role="Maire",
                   image=photo_url)
    p.add_source(MAYOR_URL)
    yield p

    resp = requests.get(COUNCIL_PAGE)
    # page rendering through JS on the client
    page_re = re.compile(r'createItemNiv3.+"District (.+?)".+(index.+)\\"')
    for district, url_rel in page_re.findall(resp.text):
        if district not in ('des Estacades', 'des Plateaux', 'des Terrasses', 'du Sanctuaire'):
            district = re.sub('\A(?:de(?: la)?|des|du) ', '', district)

        url = urljoin(COUNCIL_PAGE, url_rel)
        page = lxmlize(url)
        name = page.xpath('string(//h2)')
        email = page.xpath(
            'string(//a/@href[contains(., "mailto:")])')[len('mailto:'):]
        photo_url = page.xpath('string(//img/@src[contains(., "Conseiller")])')
        p = Person(name=name, district=district, role='Conseiller',
                       image=photo_url)
        p.add_source(url)
        p.add_contact('email', email, None)
        yield p
