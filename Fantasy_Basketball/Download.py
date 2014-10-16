#  Copyright (C) 2014 Devin Kelly
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Devin Kelly"

import pycurl
import time
import sys
import os
import errno

base_draft_url = "http://www.basketball-reference.com/draft/NBA_{year}.html"
base_team_url = "http://www.basketball-reference.com/teams/{team}/{year}.html"
default_dir = os.path.expanduser("~/.fantasy_basketball")


def mkdir_p(path):
   try:
      os.makedirs(path)
   except OSError as exc:
      if exc.errno == errno.EEXIST and os.path.isdir(path):
         pass
      else:
         raise


def download_data(data_dir, teams, drafts, league, year, league_id):
   if teams:
      downloadTeams(data_dir, year)

   if drafts:
      downloadDraft(data_dir, year)

   if (league_id) and (league_id is not None):
      downloadLeague(data_dir, leagueID, year)


def downloadDrafts(years):

   years = range(1950, 2014)
   years.reverse()

   for y in years:
      downloadDraft(y)
      time.sleep(10.0)


def downloadTeams(data_dir, year):

   teams = [u'SAS', u'OKC', u'CHI', u'BOS', u'PHO', u'MEM', u'ORL', u'NYK',
            u'PHI', u'NOH', u'UTA', u'ATL', u'DEN', u'IND', u'HOU', u'SAC',
            u'CHA', u'LAL', u'DET', u'BRK', u'MIN', u'GSW', u'TOR', u'POR',
            u'WAS', u'LAC', u'MIA', u'MIL', u'CLE', u'DAL']

   for t in teams:
      print "downloading {0}, {1}".format(t, year)
      downloadTeam(data_dir, t, year)
      time.sleep(10.0)


def downloadDraft(data_dir, year):

   data_dir = os.path.join(data_dir, "draft", str(year))
   mkdir_p(data_dir)

   filename = "draft.html"
   filename = os.path.join(data_dir, filename)

   fp = open(filename, "wb")
   curl = pycurl.Curl()
   curl.setopt(pycurl.URL, base_draft_url.format(year=year))
   curl.setopt(pycurl.FOLLOWLOCATION, 1)
   curl.setopt(pycurl.MAXREDIRS, 5)
   curl.setopt(pycurl.CONNECTTIMEOUT, 30)
   curl.setopt(pycurl.TIMEOUT, 300)
   curl.setopt(pycurl.NOSIGNAL, 1)
   curl.setopt(pycurl.WRITEDATA, fp)
   try:
      curl.perform()
   except:
      import traceback
      traceback.print_exc(file=sys.stderr)
   curl.close()
   fp.close()

   return


def downloadTeam(data_dir, team, year=time.strftime('%Y', time.localtime())):

   data_dir = os.path.join(data_dir, "teams", str(year))
   mkdir_p(data_dir)

   filename = "{team}.html".format(team=team)
   filename = os.path.join(data_dir, filename)

   fp = open(filename, "wb")
   curl = pycurl.Curl()
   curl.setopt(pycurl.URL, base_team_url.format(team=team, year=year))
   curl.setopt(pycurl.FOLLOWLOCATION, 1)
   curl.setopt(pycurl.MAXREDIRS, 5)
   curl.setopt(pycurl.CONNECTTIMEOUT, 30)
   curl.setopt(pycurl.TIMEOUT, 300)
   curl.setopt(pycurl.NOSIGNAL, 1)
   curl.setopt(pycurl.WRITEDATA, fp)
   try:
      curl.perform()
   except:
      import traceback
      traceback.print_exc(file=sys.stderr)
   curl.close()
   fp.close()

   return
