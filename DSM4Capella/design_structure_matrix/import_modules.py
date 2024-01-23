"""
/*********************************************************************
* Copyright (c) {December 2023} {Samares-Engineering} authors:[Mirna Ojeda]
*
* This program and the accompanying materials are made
* available under the terms of the Eclipse Public License 2.0
* which is available at https://www.eclipse.org/legal/epl-2.0/
*
* SPDX-License-Identifier: EPL-2.0
**********************************************************************/
"""

    
# Import genetic algorithm and DSM modules 
include('workspace://DSM4Capella/design_structure_matrix/swap_random.py')
if False:
    from Swap_random import *
    
include('workspace://DSM4Capella/design_structure_matrix/swap_random.py')
if False:
    from interactions_bw_modules import *
include('workspace://DSM4Capella/design_structure_matrix/swap_random.py')
if False:
    from Coupling_Generalised import *
include('workspace://DSM4Capella/design_structure_matrix/swap_random.py')
if False:
    from Swap_User_Defined import *
include('workspace://DSM4Capella/design_structure_matrix/swap_random.py')
if False:
    from Create_Init_Pop import *
include('workspace://DSM4Capella/design_structure_matrix/swap_random.py')
if False:
    from GeneticAlgorithm import *


#import for instantiation
include('workspace://DSM4Capella/design_structure_matrix/instantiation.py')
if False:
    from Instantiation import *
include('workspace://DSM4Capella/design_structure_matrix/instantiation.py')
if False:
    from GeneticAlgorithmConfig import *

#import capella elements retrieve from model    
include('workspace://DSM4Capella/design_structure_matrix/capella_elements_retrieve.py')
if False:
    from RetrieveCapellaElements import *  
    
#allocate functions to components result of optimized run
include('workspace://DSM4Capella/design_structure_matrix/allocate_functions_results.py')
if False:
    from LogicalArchitectureHandler import * 



