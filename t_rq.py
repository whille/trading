#!/usr/bin/env python
# encoding: utf-8

import os
import bcolz
import numpy as np

default_bundle_path = os.path.abspath(os.path.expanduser('~/.rqalpha/bundle'))
stock_path = os.path.join(default_bundle_path, 'stocks.bcolz')
dates = bcolz.open(stock_path, 'r')

assert np.any(dates[1:6]['close'] == dates['close'][1:6])
