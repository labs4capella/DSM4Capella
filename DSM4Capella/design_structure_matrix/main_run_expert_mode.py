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
# name                 : DSM4Capella expert mode
# image                : workspace://DSM4Capella/icons/GA_icon.png
# script-type          : Python
# description          : Menu to modify different parameter of genetic algorithm
# toolbar              : capella.project.explorer

loadModule('/System/UI');
loadModule('/System/UI Builder');
loadModule('/System/Resources');

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

def include_python4capella_resources():
    try:
        include('workspace://Python4Capella/simplified_api/capella.py')
        include('workspace://Python4Capella/utilities/CapellaPlatform.py')
        include('workspace://DSM4Capella/extensions/python4capellaExtendAPI.py')
        include('workspace://DSM4Capella/design_structure_matrix/import_modules.py')
        return True  # No exceptions, resources are available
    except Exception:
        
        return False  

# Check if Python4Capella resources are available
python4capella_available = include_python4capella_resources()
if python4capella_available:
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
    
    def process_dsm(functionalExchanges, allLogFunctions):
    
        matrix_function_with_interaction,dsm_with_names= RetrieveCapellaElements.initialMatrix(functionalExchanges, allLogFunctions)
        # Export in  Excel format the initial matrix
        RetrieveCapellaElements.export_matrix_to_excel(dsm_with_names, xlsx_file_name )
        return matrix_function_with_interaction
    
    def main_analysis_functions(allLogFunctions, logicalComponents, availableFunctionsDF, only_logical_components,componentExchanges):
        if availableFunctionsDF is not None:
    
            function_and_components_to_allocate, log_component_interdependecies,matrix_replaced = RetrieveCapellaElements.convert_result_in_capella_elements(
            allLogFunctions, logicalComponents, matrix_function_with_interaction, config)
            RetrieveCapellaElements.export_dsm_permutated_to_excel(matrix_replaced, xlsx_file_name_permutated )
            logical_and_functional_interdependencies=RetrieveCapellaElements.filter_interdependencies( log_component_interdependecies ,functionalExchanges)
            logical_and_functional_interdependencies,interdependencies_to_export=RetrieveCapellaElements.filter_component_exchange_missed(componentExchanges,logical_and_functional_interdependencies)
            RetrieveCapellaElements.export_allocations_to_excel(interdependencies_to_export, xlsx_file_name_for_allocations)
            function_exchange_to_allocate = RetrieveCapellaElements.filter_exchanges(componentExchanges, logical_and_functional_interdependencies)
            return function_and_components_to_allocate,function_exchange_to_allocate
        else:
            print(" -Any Functions available for allocation, stop algorithm execution")
            return None,None
    
    
    def configureUI(javaDialog, instance, result):
        if result == 0:
            # Retrieve parameters from the GUI
            initial_pop_size = int(javaDialog.getData(instance.txtInitialPopSize))
            max_num_generations = int(javaDialog.getData(instance.txtMaxNumGenerations))
            survivor_percentage = float(javaDialog.getData(instance.txtSurvivorPercentage))
            parent_percentage = float(javaDialog.getData(instance.txtParentPercentage))
            population_mutation_percentage = float(javaDialog.getData(instance.txtPopulationMutationPercentage))
            gene_mutation_percentage = float(javaDialog.getData(instance.txtGeneMutationPercentage))
    
            # Create the configuration object with GUI data
            config = GeneticAlgorithmInitialParameters(
                initial_pop_size, 
                max_num_generations, 
                survivor_percentage, 
                parent_percentage, 
                population_mutation_percentage, 
                gene_mutation_percentage
            )
        else:
            print("Dialog cancelled")
            config = GeneticAlgorithmInitialParameters()
    
        config.print_parameters()
        selectedOption = instance.evaluate(javaDialog)
        return config, selectedOption
    
    
    if __name__ == "__main__":
        start_time = time.time()
    
        print("START script execution")
        selected_element = CapellaElement(CapellaPlatform.getFirstSelectedElement())
        aird_path = '/'+ CapellaPlatform.getModelPath(selected_element)
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
        
        allLogFunctions, logicalComponents, allAllocatedFunctions, availableFunctionsDF, only_logical_components,functionalExchanges,componentExchanges = get_capella_elements(lf, lc)
        if functionalExchanges is not None and allLogFunctions is not None:
            instance = GeneticAlgorithmDialog()
            javaDialog = createDialog("instance.build()", "Genetic Algorithm Parameters", "Genetic algorithm parameters and design structure matrix analysis")
            result = executeUI("javaDialog.open()");  
            config, selectedOption=configureUI(javaDialog, instance, result)
            
            if selectedOption=="Analysis":
                matrix_function_with_interaction = process_dsm(functionalExchanges, allLogFunctions)
                function_and_components_to_allocate,function_exchange_to_allocate = main_analysis_functions(allLogFunctions, logicalComponents, availableFunctionsDF, only_logical_components,componentExchanges)
            
            elif selectedOption=="Optimization":
                matrix_function_with_interaction = process_dsm(functionalExchanges, allLogFunctions)
                function_and_components_to_allocate,function_exchange_to_allocate = main_analysis_functions(allLogFunctions, logicalComponents, availableFunctionsDF, only_logical_components,componentExchanges)
                RetrieveCapellaElements.create_allocations(function_and_components_to_allocate, function_exchange_to_allocate)
            else:
                print("Selected option not found")
            CapellaPlatform.refresh(folder)
            
        else:
            if functionalExchanges is None:
                print("- Any functional exchange found to create DSM")
            
        
        print(f"--END script execution, time elapsed: {time.time() - start_time:.2f} seconds")

else:
    print("ERROR: Python4Capella resource is missing in the workspace.")