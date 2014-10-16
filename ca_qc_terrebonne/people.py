# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.terrebonne.qc.ca/ville_conseil-municipal_conseillers-municipaux.php'


class TerrebonnePersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE, encoding='latin-1')
    for councillor_elem in page.xpath('//div[@class="protraits"]')[0]:
      district, name, phone = councillor_elem.xpath('./span/text()')[:3]
      photo_url = councillor_elem[0].attrib['src']
      # email is form-based
      p = Person(name=name, district=district, role='Conseiller',
                     image=photo_url)
      p.add_source(COUNCIL_PAGE)
      yield p
    mayor_elem = page.xpath('//div[@class="protraits maire"]')[0][0]
    name = mayor_elem.xpath('./span/text()')[1]
    photo_url = mayor_elem[0].attrib['src']
    p = Person(name=name, district='Terrebonne', role='Maire',
                   image=photo_url)
    p.add_source(COUNCIL_PAGE)
    yield p
