# -*- coding: utf-8 -*-
"""
Created on Tue Feb 04 12:39:14 2014

@author: fh
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:18:27 2013

@author: RIGAUD Thomas
"""
from numpy import array

isoflexor = array([
[150],
[130],
[40]
])



norm_factor = isoflexor[1,:]

isoflexor_normalized = isoflexor/norm_factor
