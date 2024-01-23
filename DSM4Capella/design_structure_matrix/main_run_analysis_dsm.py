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
# name                 : Architecture Analysis with DSM
# image                : workspace://DSM4Capella/icons/dsm_icon.png
# script-type          : Python
# description          : analysis of logical architecture with dsm approach
# popup                : enableFor(org.polarsys.capella.core.data.la.LogicalArchitecture)
#python library imports
import numpy as np
import pandas as pd
import time, random
import itertools 
import openpyxl
from openpyxl.styles import Border, Side, Alignment,PatternFill
from openpyxl.utils import get_column_letter
from itertools import cycle
from collections import defaultdict
random.seed(25)


# Module imports
include('workspace://Python4Capella/simplified_api/capella.py')
if False:
    from simplified_api.capella import *

include('workspace://Python4Capella/utilities/CapellaPlatform.py')
if False:
    from utilities.CapellaPlatform import *

include('workspace://DSM4Capella/extensions/python4capellaExtendAPI.py')
if False:
    from extensions.python4capellaExtendAPI import *

include('workspace://DSM4Capella/design_structure_matrix/import_modules.py')
if False:
    from design_structure_matrix.import_modules import *


def get_capella_elements(lf, lc):
    allLogFunctions, availableFunctionsDF = RetrieveCapellaElements.getLogicalFunctionAvailableToAllocation(lf)
    logicalComponents, allAllocatedFunctions, only_logical_components = RetrieveCapellaElements.getAllLogicalComponents(lc)
    
    allLogFunctions, logicalComponents = RetrieveCapellaElements.update_allocation_status(allLogFunctions, logicalComponents)
    functionalExchanges = RetrieveCapellaElements.getAllFunctionalExchange(lf)
    componentExchanges = RetrieveCapellaElements.get_component_interactions(lc)
    return allLogFunctions, logicalComponents, allAllocatedFunctions, availableFunctionsDF, only_logical_components,functionalExchanges,componentExchanges

def main_functions(allLogFunctions, logicalComponents, availableFunctionsDF, only_logical_components,componentExchanges):
    if availableFunctionsDF is None:
        print("--All LogicalFunctions already allocated--")
        
        return
    
    if allLogFunctions is None or only_logical_components is None:
        print("** Any LogicalFunctions available for allocation or any LogicalComponents found in model")
        return

    matrix_function_with_interaction,dsm_with_names= RetrieveCapellaElements.initialMatrix(functionalExchanges, allLogFunctions)
    # Export in  Excel format the initial matrix
    RetrieveCapellaElements.export_matrix_to_excel(dsm_with_names, xlsx_file_name )

    
    config=GeneticAlgorithmInitialParameters(xlsx_path)
    config.print_parameters()
    function_and_components_to_allocate, log_component_interdependecies,matrix_replaced = RetrieveCapellaElements.convert_result_in_capella_elements(
        allLogFunctions, logicalComponents, matrix_function_with_interaction, config)
    RetrieveCapellaElements.export_dsm_permutated_to_excel(matrix_replaced, xlsx_file_name_permutated )
    logical_and_functional_interdependencies=RetrieveCapellaElements.filter_interdependencies( log_component_interdependecies ,functionalExchanges)
    logical_and_functional_interdependencies,interdependencies_to_export=RetrieveCapellaElements.filter_component_exchange_missed(componentExchanges,logical_and_functional_interdependencies)
    RetrieveCapellaElements.export_allocations_to_excel(interdependencies_to_export, xlsx_file_name_for_allocations)
    function_exchange_to_allocate = RetrieveCapellaElements.filter_exchanges(componentExchanges, logical_and_functional_interdependencies)
    print("--END  architecture analysis made by Design Structure Matrix with Genetic Algorithm--")
   
if __name__ == "__main__":
    start_time = time.time()

    print("START script execution")
    selected_element = CapellaElement(CapellaPlatform.getFirstSelectedElement())
    aird_path = '/'+ CapellaPlatform.getModelPath(selected_element)
    xlsx_path = "/DSM4Capella/Resources/parametersGA_initialization.xlsx"
    model = CapellaModel()
    model.open(aird_path)

    #create folder to export excel file
    project_name = aird_path[0:(aird_path.index("/", 1) + 1)]
    project = CapellaPlatform.getProject(project_name)
    folder = CapellaPlatform.getFolder(project, 'Results')
    xlsx_file_name = CapellaPlatform.getAbsolutePath(folder) + '/' + 'DSM_Initial_LA.xlsx'  
    xlsx_file_name_permutated = CapellaPlatform.getAbsolutePath(folder) + '/' + 'DSM_Permutated_LA.xlsx' 
    xlsx_file_name_for_allocations = CapellaPlatform.getAbsolutePath(folder) + '/' + 'LogicalArchitectureProposed.xlsx' 
    se = model.get_system_engineering()
    print("Capella model: ", se.get_name())

    lf = se.get_logical_architecture().get_logical_function_pkg()
    lc = se.get_logical_architecture().get_logical_component_pkg()
    
    allLogFunctions, logicalComponents, _, availableFunctionsDF, only_logical_components,functionalExchanges,componentExchanges  = get_capella_elements(lf, lc)
    main_functions(allLogFunctions, logicalComponents, availableFunctionsDF, only_logical_components,componentExchanges)
    CapellaPlatform.refresh(folder)
    
    print(f"--END script execution, time elapsed: {time.time() - start_time:.2f} seconds")
