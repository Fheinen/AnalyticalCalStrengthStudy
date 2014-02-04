# -*- coding: utf-8 -*-
"""
Created on Mon Feb 03 13:32:50 2014

@author: fh
"""


from __future__ import division
from os import getcwd, path as op
from numpy import array, sqrt, mean, zeros
from anypytools.abcutils import AnyPyProcess
from scipy.optimize import fmin_l_bfgs_b

global iteration_counter
iteration_counter = 0


def setup_study(designvars):
    if designvars is None:
        designvars = array([0.5, 1.2])
    basepath = op.join( getcwd(), '..')
    app = AnyPyProcess(basepath, anybodycon_path = "F:\Program Files\AnyBody Technology\AnyBody.6.0\AnyBodyCon.exe", disp = False)
    loadmacro = 'load "Demo.Forces.main.any"'
    macrocmds = ['operation RunApplication', 'run']
    inputs = [('Main.DesignVars.bb_rmin', designvars[0]),
              ('Main.DesignVars.bb_rmax', designvars[1])
              ]
    outputs =  ['Main.ElbowIsomStrength.Output.Strength.Val']
    return (app, loadmacro, macrocmds, inputs, outputs)

def eval_w_gradient(designvars,*arg):
    pertubation_factor = 10e-4
    global iteration_counter
    iteration_counter += 1
    print iteration_counter, 'Design vars:', designvars
    (app, loadmacro, macrocmds, inputs,outputs) = setup_study(designvars)
    (res, pert) = app.start_pertubation_job(loadmacro, macrocmds, inputs, outputs,
                              perturb_factor = pertubation_factor)
    key_isoflex = outputs[0]
    pertubations = zeros((len(designvars,)))
    for i in range(len(designvars)):
        pertubations[i] = metric(pert[key_isoflex][i])
    objective = metric(res[key_isoflex])
    gradient = (pertubations-objective)/pertubation_factor
    print 'Objective:', objective
    print 'Gradient:', gradient
    return objective, gradient

def metric(c_isoflex):
    if isinstance(c_isoflex, list):
        c_isoflex = c_isoflex[0]
 
    import experimental_data_L6 as data
    
    m_isoflex = mean(data.isoflexor_normalized,1)


    norm_factor = c_isoflex[1]
    c_isoflex = c_isoflex/norm_factor


    try:
        ss_isoflex = sum(((c_isoflex-m_isoflex)/m_isoflex)**2)

    except TypeError:
        print 'Error in metric. Return 100'
        return 100
    N_total = len(m_isoflex)
    weight = float(N_total) / array([len(m_isoflex)])
    return sqrt(ss_isoflex*weight[0])





if __name__ == '__main__':
    x0 = array([0.5, 1.4])
    bounds = [(0.1,0.7), (1,1.6)] 
    epsilon = 1e-4
    (x,f,d) =  fmin_l_bfgs_b(func = eval_w_gradient, x0 = x0, args=(epsilon,), bounds = bounds)
#(x,nfeval,rc) = fmin_tnc(func = evaluate, x0 = x0, fprime = gradient, args=(epsilon,), bounds = bounds, maxCGit=0,  eta=-1, stepmx=0.05, disp=1)