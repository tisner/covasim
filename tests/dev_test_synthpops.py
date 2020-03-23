'''
Test different population options
'''

#%% Imports and settings
import pylab as pl
import sciris as sc
import covasim as cova
try:
    import synthpops as sp
except:
    print('Synthpops import failed')

doplot = 1


#%% Define the tests

def test_import():
    sc.heading('Testing imports')

    assert cova._requirements.available['synthpops'] == True
    import synthpops as sp
    print(sp.datadir)

    return


def test_pop_options(doplot=False): # If being run via pytest, turn off
    sc.heading('Basic populations tests')

    popchoices = ['random', 'bayesian']
    if sp.config.full_data_available:
        popchoices.append('data')

    basepars = {
        'n': 3000,
        'n_infected': 10,
        'contacts': 20,
        'n_days': 90
        }

    sims = sc.objdict()
    for popchoice in popchoices:
        sc.heading(f'Running {popchoice}')
        sims[popchoice] = cova.Sim()
        sims[popchoice].update_pars(basepars)
        sims[popchoice]['usepopdata'] = popchoice
        sims[popchoice].run()

    if doplot:
        for key,sim in sims.items():
            sim.plot()
            pl.gcf().axes[0].set_title(f'Counts: {key}')

    return sims



def test_interventions(doplot=False): # If being run via pytest, turn off
    sc.heading('Test interventions')

    popchoice = 'bayesian'
    intervs = ['none', 'all', 'school', 'work', 'comm']
    interv_days = [21]

    basepars = {
        'n': 10000,
        'n_infected': 100,
        'n_days': 60
        }

    def interv_func(sim, t, interv):
        if   interv == 'none':   sim['beta'] *= 1.0
        elif interv == 'all':    sim['beta'] *= 0.1
        elif interv == 'school': sim['beta_pop']['S'] = 0
        elif interv == 'work':   sim['beta_pop']['W'] = 0
        elif interv == 'comm':   sim['beta_pop']['R'] = 0
        else:
            raise KeyError(interv)
        return sim

    sims = sc.objdict()
    for interv in intervs:
        sc.heading(f'Running {interv}')
        interv_lambda = lambda sim,t: interv_func(sim=sim, t=t, interv=interv)
        sims[interv] = cova.Sim()
        sims[interv].update_pars(basepars)
        sims[interv]['usepopdata'] = popchoice
        sims[interv]['interv_days'] = interv_days
        sims[interv]['interv_func'] = interv_lambda
        sims[interv].run()

    if doplot:
        for key,sim in sims.items():
            sim.plot()
            pl.gcf().axes[0].set_title(f'Counts: {key}')

    return sims



#%% Run as a script
if __name__ == '__main__':
    sc.tic()

    # test_import()
    # sims1 = test_pop_options(doplot=doplot)
    sims2 = test_interventions(doplot=doplot)

    sc.toc()


print('Done.')
