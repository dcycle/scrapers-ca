from utils import CanadianJurisdiction


class Peterborough(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3515014/council'
  geographic_code = 3515014

  def _get_metadata(self):
    return {
      'name': 'Peterborough',
      'legislature_name': 'Peterborough City Council',
      'legislature_url': 'http://www.city.peterborough.on.ca',
    }
