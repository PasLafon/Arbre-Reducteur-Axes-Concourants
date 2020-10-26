#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:08:26 2020

@author: pascal.lafon@utt.fr
"""

import numpy as np
import matplotlib.pyplot as plt

def TraceGrapheCohesion(figsize,npts,intervalles,expressions):
    '''
    |
    +->TraceGrapheCohesion : tracé des graphes de cohésion dans une poutre

    Parameters
    ----------
    figsize : tuple
        Taille de la figure en pouces ex : (12,12)
    npts : int
        Le nombre de points par intervalle
    intervalles : tuple de tuple ((a,b),(c,d))
        Les bornes de chaque intervalle graphe
    expressions : dictionnaire des expressions des efforts de cohésion
        {'N'  :(exp1,exp2,...),
         'Ty' :(exp1,exp2,...),
         'Tz' :(exp1,exp2,...),
         'Mt' :(exp1,exp2,...),
         'Mfy':(exp1,exp2,...),
         'Mfz':(exp1,exp2,...)}
        exp du type lambda x:F*(a-x)
        Attention de nombre d'expressions par sollicitation doit être
        cohérent avec le nombre d'intervalles
    Returns
    -------
    None.
    '''    
    # Titre des graphes ...
    LabelsAxeY = {'N'  :r'$N(x)$ en [N]',
                 'Ty'  :r'$T_y(x)$ en [N]',
                 'Tz'  :r'$T_z(x)$ en [N]',
                 'Mt'  :r'$M_t(x)$ en [N.m]',
                 'Mfy' :r'$M_{fy}(x)$ en [N.m]',
                 'Mfz' :r'$M_{fz}(x)$ en [N.m]'}
    # Couleurs des graphes ....
    Couleurs = {'N'  :'olive',
                'Ty' :'blue',
                'Tz' :'cyan',
                'Mt' :'orange',
                'Mfy':'purple',
                'Mfz':'red'}
    # Prepare la figure ...-> nb de tracé = nb d'expressions fournies
    nbgraph = len(expressions)
    fig=plt.figure(figsize=figsize,constrained_layout=True)
    axs = fig.subplots(nbgraph,1,sharex=True)
    # Pour chaque expression dans expressions      
    for igraph,soll in enumerate(expressions):
#%%
        expression = expressions[soll]
        LabelY = LabelsAxeY[soll]
        xtickgraph = []
        # Construit les ticks de l'axe des abscisses ...
        for xtickint in intervalles:
            for xtick in xtickint:
                xtickgraph.append(xtick)
        # Elmine les doublons éventuels ...        
        xtickgraph = np.array(list(dict.fromkeys(xtickgraph)),dtype=float)        
#%%
        # Pour chaque intervalle dans expression :
        for nint,exp_int in enumerate(expression):
            # Vecteur d'abcisses pour tracé -> xint
            xint = np.linspace(intervalles[nint][0],intervalles[nint][-1],npts)
            # Valeur suivant exp_int (fonction) -> yint
            yint =exp_int(xint)
            if isinstance(yint,np.ndarray):
                # Le resultat est un array : on prend les valeurs de début et de fin
                # pour les ticks sur y ...
                # on pourrait prendre aussi les maximums lorsque différents
                # du début de la fin ...
                ytickint = yint[[0,-1]]
            else:
                # Le résultat est un scalaire -> fabrique un array de la même
                # taille que xint ..
                ytickint = yint
                yint = np.full_like(xint,yint)
            # Premier intervalle : initialise :
            # xgraph -> vecteur d'abcisses sur tout le graphe (pour tous les intervalles)
            # ytickgraph -> ytick pour tout le graphe ...
            if nint==0:
                xgraph = xint
                ygraph = yint
                ytickgraph = ytickint
            else:
                xgraph = np.hstack([xgraph,np.NaN,xint])
                ygraph = np.hstack([ygraph,np.NaN,yint])
                ytickgraph = np.hstack([ytickgraph,ytickint])
        # Trie les ytick ...
        ytickgraph = np.hstack([ytickgraph,0])        
        ytickgraph.sort()         
#%%
        # Tracé ...
        axs[igraph].set_xticks(xtickgraph)
        axs[igraph].set_yticks(ytickgraph)
        axs[igraph].set_xlim(xgraph[0],xgraph[-1])
        axs[igraph].set_title(LabelY,color=Couleurs[soll])
        axs[igraph].plot(xgraph,ygraph,color=Couleurs[soll])
        axs[igraph].fill_between(xgraph,ygraph,facecolor=Couleurs[soll],alpha=0.1)
        axs[igraph].grid()
          