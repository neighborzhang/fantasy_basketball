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
import json
import pandas as pd
import numpy as np

from Util import mkdir_p

import matplotlib.pyplot as plt
import re


class Plotter(object):

    def __init__(self, data_dir, year):
        default_processed_data_dir = os.path.join(data_dir, 'processed_data')
        default_plot_dir = os.path.join(data_dir, 'plots')
        self.save_dir = os.path.join(default_plot_dir, year)
        fname = os.path.join(default_processed_data_dir, year, 'team_data.pkl')

        self.df = pd.read_pickle(fname)
        self.year = year

        self.make_positional_df()

        mkdir_p(self.save_dir)

    def make_positional_df(self):
        self.C = self.df[self.df.Pos == 'C']
        self.PF = self.df[self.df.Pos == 'PF']
        self.SF = self.df[self.df.Pos == 'SF']
        self.SG = self.df[self.df.Pos == 'SG']
        self.PG = self.df[self.df.Pos == 'PG']

    def is_plot_func(self, s):
        if re.search("^plot_", s) is not None:
            attr = getattr(self, s)
            if callable(attr):
                return True

        return False

    def make_all_plots(self, img_format='eps'):

        attrs = dir(self)

        plot_funcs = [x for x in attrs if self.is_plot_func(x)]

        for func in plot_funcs:
            f = getattr(self, func)
            f(img_format)

    def plot_value_hist(self, img_format="eps"):

        # FIXME - best way to get x-y data?
        plot_data = {'xlabel': 'Frequency',
                     'ylabel': 'Value',
                     'title': 'Value Histogram',
                     'x': [0],
                     'y': [0]}

        self.df.hist('value', bins=20)

        fig = plt.gcf()
        ax = plt.gca()
        ax.set_ylabel(plot_data['xlabel'])
        ax.set_xlabel(plot_data['ylabel'])
        ax.set_title(plot_data['title'])
        fname = "value_histogram.{0}".format(img_format)
        fig.savefig(os.path.join(self.save_dir, fname))

        fname = "value_histogram.json"
        with open(os.path.join(self.save_dir, fname), 'w') as fd:
            fd.write(json.dumps(plot_data))

    def plot_stats_hist(self, img_format="eps"):

        stats = ['FG%', 'FT%', 'TRB', 'AST', 'BLK', 'PTS']

        for stat in stats:
            # FIXME - best way to get x-y data?
            plot_data = {'xlabel': stat,
                         'ylabel': 'Frequency',
                         'title': '{0} Histogram'.format(stat),
                         'x': [0],
                         'y': [0]}

            self.df.hist(stat, bins=20)
            fig = plt.gcf()
            ax = plt.gca()
            ax.set_xlabel(plot_data['xlabel'])
            ax.set_ylabel(plot_data['ylabel'])
            ax.set_title(plot_data['title'])
            fname = "{0}_histogram.{1}".format(stat, img_format)
            fig.savefig(os.path.join(self.save_dir, fname))

            fname = "{0}_histogram.json".format(stat)
            with open(os.path.join(self.save_dir, fname), 'w') as fd:
                fd.write(json.dumps(plot_data))

    def plot_value_hist_by_pos(self, img_format="eps"):

        for pos in ['C', 'PF', 'SF', 'SG', 'PG']:
            # FIXME - best way to get x-y data?
            plot_data = {'xlabel': 'Value',
                         'ylabel': 'Frequency',
                         'title': 'Value Histogram for {0}'.format(pos),
                         'x': [0],
                         'y': [0]}
            df = getattr(self, pos)
            df.hist('value', bins=20)
            fig = plt.gcf()
            ax = plt.gca()
            ax.set_xlabel(plot_data['xlabel'])
            ax.set_ylabel(plot_data['ylabel'])
            ax.set_title(plot_data['title'])
            fname = "value_histogram_{0}.{1}".format(pos, img_format)
            fig.savefig(os.path.join(self.save_dir, fname))

            fname = "value_histogram_{0}.json".format(pos)
            with open(os.path.join(self.save_dir, fname), 'w') as fd:
                fd.write(json.dumps(plot_data))

    def plot_value_by_pos(self, img_format="eps"):

        C_avg_value = self.C.mean()['value']
        PF_avg_value = self.PF.mean()['value']
        SF_avg_value = self.SF.mean()['value']
        SG_avg_value = self.SG.mean()['value']
        PG_avg_value = self.PG.mean()['value']

        y = (C_avg_value,
             PF_avg_value,
             SF_avg_value,
             SG_avg_value,
             PG_avg_value)
        N = 5
        width = 0.5
        ind = np.arange(N)  # the x locations for the groups

        plot_data = {'xlabel': 'Position',
                     'ylabel': 'Average Value',
                     'title': 'Average Value by Position',
                     'x': ind.tolist(),
                     'y': y}

        fig, ax = plt.subplots()
        ax.bar(ind, y)

        # add some text for labels, title and axes ticks
        ax.set_xlabel(plot_data['xlabel'])
        ax.set_ylabel(plot_data['ylabel'])
        ax.set_title(plot_data['title'])
        ax.set_xticks(ind + width)
        ax.set_xticklabels(('C', 'PF', 'SF', 'SG', 'PG'))

        fname = "value_by_pos.{0}".format(img_format)
        fig.savefig(os.path.join(self.save_dir, fname))

        fname = "value_by_pos.json"
        with open(os.path.join(self.save_dir, fname), 'w') as fd:
            fd.write(json.dumps(plot_data))

    def plot_top_50_by_pos(self, img_format="eps"):
        top_50 = self.df.sort('value', ascending=False)[0:50]

        C = sum(top_50.Pos == 'C')
        PF = sum(top_50.Pos == 'PF')
        SF = sum(top_50.Pos == 'SF')
        SG = sum(top_50.Pos == 'SG')
        PG = sum(top_50.Pos == 'PG')

        y = [C, PF, SF, SG, PG]

        N = 5
        width = 0.5

        ind = np.arange(N)  # the x locations for the groups

        plot_data = {'xlabel': 'Number of Players',
                     'ylabel': 'Position',
                     'title': 'Top 50 players value, by position',
                     'x': ind.tolist(),
                     'y': y}

        fig, ax = plt.subplots()
        ax.bar(ind, y)

        # add some text for labels, title and axes ticks
        ax.set_ylabel(plot_data['xlabel'])
        ax.set_xlabel(plot_data['ylabel'])
        ax.set_title(plot_data['title'])
        ax.set_xticks(ind + width)
        ax.set_xticklabels(('C', 'PF', 'SF', 'SG', 'PG'))

        fname = "top_50_value_by_pos.{0}".format(img_format)
        fig.savefig(os.path.join(self.save_dir, fname))

        fname = "top_50_value_by_pos.json"
        with open(os.path.join(self.save_dir, fname), 'w') as fd:
            fd.write(json.dumps(plot_data))
