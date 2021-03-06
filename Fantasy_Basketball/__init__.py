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


import os
from Download import download_data
from Process import get_player_stats
from Process import get_fantasy_teams
from Plot import Plotter
from Util import mkdir_p
from Web import Web
from ESPN_League import ESPN_League

# Use asserts to silence PEP8... kludgy
assert download_data
assert get_player_stats
assert get_fantasy_teams
assert Plotter
assert mkdir_p
assert Web
assert ESPN_League


default_dir = os.path.expanduser("~/.fantasy_basketball")
default_raw_data_dir = os.path.join(default_dir, "raw_data")
default_processed_data_dir = os.path.join(default_dir, "processed_data")
default_html_dir = os.path.join(default_dir, "html")
default_plot_dir = os.path.join(default_dir, "plot")
