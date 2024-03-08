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
class RetrieveCapellaElements:

    @staticmethod
    def recurse_logical_functions(func, all_log_funcs, available_funcs):
        children = func.get_children_logical_functions()
        if children:
            for child_func in children:
                RetrieveCapellaElements.recurse_logical_functions(child_func, all_log_funcs, available_funcs)
        else:
            all_log_funcs.append((func.get_name(), func))
            if func.get_allocating_component() is None:
                available_funcs.append((func.get_name(), func))
    
    @staticmethod
    def create_dataframe(data, columns):
        return pd.DataFrame(data, columns=columns) if data else None
    
    @staticmethod
    def getLogicalFunctionAvailableToAllocation(lf):
        all_log_funcs, available_funcs = [], []
        root_func_name_prefix = 'Root '
        
        for func in lf.get_owned_logical_functions():
            if func.get_name().startswith(root_func_name_prefix):
                RetrieveCapellaElements.recurse_logical_functions(func, all_log_funcs, available_funcs)
        
        # Convert lists to DataFrames if they are not empty
        allLogFunctions = RetrieveCapellaElements.create_dataframe(all_log_funcs, ['LogicalFunc_name', 'LogFunc_Java'])
        availableFunctionsDF = RetrieveCapellaElements.create_dataframe(available_funcs, ['LogicalFunc_name', 'LogFunc_Java'])
        
        # Log and add additional data if DataFrame exists
        if allLogFunctions is not None:
            allLogFunctions['Func_index'] = allLogFunctions.index
            allLogFunctions['Allocation_Status'] = 'Available'
            allLogFunctions['Component_index'] = -1
            allLogFunctions['Component_name'] = None
            allLogFunctions['Component_instance'] = None
        else:
            print("- All Logical Functions are already allocated.")
        
        return allLogFunctions, availableFunctionsDF
    @staticmethod
    def data_process(all_info):
        logical_components = pd.DataFrame(all_info, columns=['LogicalComponent_name', 'LogComponent_Java', 'AllocatedFunctions'])
        allocated_functions = logical_components[logical_components['AllocatedFunctions'].str.len() > 0]
        logical_components['Comp_index'] = np.arange(1, len(logical_components) + 1)
        only_logical_components = logical_components[logical_components['LogComponent_Java'].apply(lambda x: isinstance(x, LogicalComponent))]
        if len(logical_components) >= 10:
            comp_index_10_row = logical_components.loc[logical_components['Comp_index'] == 10].iloc[0]
            valid_rows = logical_components[logical_components['LogComponent_Java'].apply(lambda x: isinstance(x, LogicalComponent))]
            
            if not valid_rows.empty:
                valid_row = valid_rows.iloc[0]
                target_index = valid_row.name
                logical_components.at[target_index, 'Comp_index'], logical_components.at[comp_index_10_row.name, 'Comp_index'] = \
                logical_components.at[comp_index_10_row.name, 'Comp_index'], logical_components.at[target_index, 'Comp_index']
            else:
                pass
        else:
            logical_components=logical_components
        return logical_components, allocated_functions, only_logical_components
    @staticmethod
    def extract_allocated_functions(component):
        allocated_functions = component.get_allocated_functions()
        if allocated_functions:
            return [func.get_name() for func in allocated_functions]
        else:
            return None
    @staticmethod
    def process_logical_system(lc1):
        all_names = []
        if lc1 is not None:
            # Check if the current component is the lowest level (no owned logical components)
            if not lc1.get_owned_logical_components():
                allocated_functions = RetrieveCapellaElements.extract_allocated_functions(lc1)
                all_names.append(( lc1.get_name(),lc1, allocated_functions))
            else:
                # If the current component has owned logical components, process them recursively
                for sub_component in lc1.get_owned_logical_components():
                    all_names.extend(RetrieveCapellaElements.process_logical_system(sub_component))
        return all_names
    @staticmethod
    def getAllLogicalComponents(lc):
        all_names = []
        for lc1 in lc.get_owned_logical_components():
            if isinstance(lc1, LogicalSystem):
                all_names.extend(RetrieveCapellaElements.process_logical_system(lc1))
            elif isinstance(lc1, LogicalActor):
                allocated_functions = lc1.get_allocated_functions()
                if allocated_functions:
                    allocated_functions_names = [func.get_name() for func in allocated_functions]
                    all_names.append((lc1.get_name(),lc1, allocated_functions_names))
                    
        logical_components,allocated_functions,only_logical_components=RetrieveCapellaElements.data_process(all_names)

        return logical_components, allocated_functions, only_logical_components

 
    @staticmethod 
    def update_allocation_status(functions_df, allocated_df):
        # Create a mapping of function names to their corresponding Comp_index and Component_name
        Log_Components = allocated_df
        #Log_Components = allocated_df[allocated_df['LogComponent_Java'].apply(lambda x: isinstance(x, LogicalComponent))]
        func_to_comp_map = {}
        func_to_comp_instance_map = {}
        
        # Check if 'AllocatedFunctions' exists in DataFrame
        if 'AllocatedFunctions' in allocated_df.columns:
            for index, row in allocated_df.iterrows():
                allocated_functions = row['AllocatedFunctions']
                # Check if allocated_functions is not None and is iterable
                if allocated_functions is not None:
                    for func_name in allocated_functions:
                        func_to_comp_map[func_name] = (row['Comp_index'], row['LogicalComponent_name'])
                        func_to_comp_instance_map[func_name] = row['LogComponent_Java']
                    
        def set_allocation_status_and_comp_index(row):
            func_name = row['LogicalFunc_name']
            if func_name in func_to_comp_map:
                row['Allocation_Status'] = 'Not_Available'
                row['Component_index'], row['Component_name'] = func_to_comp_map[func_name]
            else:
                row['Allocation_Status'] = 'Available'
            return row
    
        # Apply the function to your DataFrame
        functions_df = functions_df.apply(set_allocation_status_and_comp_index, axis=1)
        # Update Component_instance values
        functions_df['Component_instance'] = functions_df['LogicalFunc_name'].map(func_to_comp_instance_map).fillna(functions_df['Component_instance'])

        return functions_df, Log_Components

    @staticmethod
    def getAllFunctionalExchange(lf):
        functionalExchanges=None
        allInteractions=[]
        #retrieve FunctionalExchange with FunctionPort and its Source/target function
        for fe in lf.get_all_contents_by_type(FunctionalExchange):
            if fe is not None:
                funcExch_name=fe.get_name()
                #retrieving source 
                if fe.get_source_port() and fe.get_target_port() is not None:
                    source_function=fe.get_source_function()
                    source_port=fe.get_source_port()
                    #retrieving target
                    target_function=fe.get_target_function()
                    target_port = fe.get_target_port()
                    allInteractions.append((funcExch_name,source_function.get_name(),source_port.get_name(),target_function.get_name(),target_port.get_name(),fe))
                functionalExchanges=pd.DataFrame(allInteractions)
                functionalExchanges.columns= ['FunctionalExchange_name', 'SourceFunction', 'FunctionOutputPort', 'TargetFunction', 'FunctionInputPort', 'FunctionalExchangeJavaObject']
        print("- Retrieved all Connections from model")
        #print(functionalExchanges.to_string())
        return functionalExchanges
    
    @staticmethod
    def create_matrix(names):
        N = len(names)
        matrix = np.zeros((N, N))
        return matrix
    @staticmethod
    def initialMatrix(functionalExchanges, Functions):
        matrix_function_with_interaction = None
        
        if functionalExchanges is not None and Functions is not None:
            names = Functions['LogicalFunc_name']
            matrix_function_with_interaction = RetrieveCapellaElements.create_matrix(names)
            name_to_index = {name: index for index, name in enumerate(names)}

            for _, row in functionalExchanges.iterrows():
                source_function = row['SourceFunction']
                target_function = row['TargetFunction']
                
                if target_function != source_function:
                    if target_function in name_to_index and source_function in name_to_index:
                        source_index = name_to_index[source_function]
                        target_index = name_to_index[target_function]
                        matrix_function_with_interaction[source_index, target_index] = 1
        dsm_with_names = pd.DataFrame(matrix_function_with_interaction, index=names, columns=names, dtype=object)
        # Fill diagonal values with F1, F2, F3, ...
        for i in range(len(names)):
            dsm_with_names.iloc[i, i] = f"F{i+1}"
        
        return matrix_function_with_interaction, dsm_with_names

    @staticmethod
    def export_matrix_to_excel(matrix, file_name, fixed_width=20):
        sheet_name = 'DSM_of_LogicalArchitecture'
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            matrix.to_excel(writer, sheet_name=sheet_name, index=True, header=True)
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            thin_border_side = Side(style='thin')
            thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

            fill_color = PatternFill(start_color='070C13', end_color='070C13', fill_type='solid')

            for col in range(1, len(matrix.columns) + 2):  
                header_cell = worksheet.cell(row=1, column=col)
                header_cell.alignment = Alignment(wrap_text=True, horizontal='center')
                header_cell.border = Border(left=Side(style='thick'), right=Side(style='thick'), top=Side(style='thick'), bottom=Side(style='thick'))
                worksheet.column_dimensions[get_column_letter(col)].width = fixed_width
            first_column_width = max(len(str(cell.value)) for cell in worksheet["A"]) + 2 
            worksheet.column_dimensions['A'].width = first_column_width
            cell_a1 = worksheet.cell(row=1, column=1)
            cell_a1.alignment = Alignment(horizontal='center', vertical='center')

            for i in range(2, len(matrix) + 2):
                cell = worksheet.cell(row=i, column=i)
                if isinstance(cell.value, str) and cell.value.startswith('F'):
                    cell.fill = fill_color

                for row in worksheet.iter_rows(min_row=2, max_row=len(matrix) + 1, min_col=1, max_col=len(matrix.columns) + 1):
                    for cell in row:
                        cell.border = thin_border
                        cell.alignment = Alignment(horizontal='left')
        print("Exported the initial DSM of capella model under the Results file")
    @staticmethod
    def randomly_select_row_if_more_one_optimal_result(resulting_chromosomes):
        if resulting_chromosomes.shape[0] > 1:
            resulting_chromosomes = resulting_chromosomes.sample(1)
            
        else:
            pass
        return resulting_chromosomes

    @staticmethod
    def melt_and_map_chromosomes(resulting_chromosomes, allLogFunctions):
        
        melted = pd.melt(resulting_chromosomes.reset_index(), id_vars='index', var_name='LogicalFunc_name', value_name='Components_name')
        melted = pd.merge(melted, allLogFunctions, on='LogicalFunc_name', how='left')
    
        melted['LogFunctions_name'] = melted['LogicalFunc_name']
        
        name_to_java_mapping = dict(zip(allLogFunctions['LogicalFunc_name'], allLogFunctions['LogFunc_Java']))
        melted['LogicalFunc_name'] = melted['LogicalFunc_name'].map(name_to_java_mapping).fillna(melted['LogicalFunc_name'])
        #filter only functions available to allocate
        melted = melted[melted['Allocation_Status'] == 'Available']
        
        return melted
    
    @staticmethod
    def merge_data(melted, logicalComponents):
        logicalComponents['LogicalComponent_name'] = logicalComponents['LogicalComponent_name'].astype(str)
        merged_data = pd.merge(melted, logicalComponents, left_on='Components_name', right_on='LogicalComponent_name', how='left')
        merged_data['Components_name'] = merged_data['LogComponent_Java']
        return merged_data[['index', 'LogicalFunc_name', 'Components_name']]

    @staticmethod
    def convert_result_in_capella_elements(allLogFunctions, logicalComponents, matrix_function_with_interaction, config: GeneticAlgorithmInitialParameters):
        """
        Convert the results from the genetic algorithm into Capella elements.
        
        :param allLogFunctions: Description of this parameter
        :param logicalComponents: Description of this parameter
        :param matrix_function_with_interaction: Description of this parameter
        :param config: Genetic algorithm initial parameters
        """
        # Run the genetic algorithm process
        resulting_chromosomes, opt_chromosome = Instantiation.run_algorithm_process(allLogFunctions, logicalComponents, matrix_function_with_interaction, config)
        new_matrix = RetrieveCapellaElements.integrate_and_reorder_matrix(opt_chromosome, matrix_function_with_interaction)
        matrix = RetrieveCapellaElements.replace_last_row_values(new_matrix, logicalComponents)
        matrix_replaced = RetrieveCapellaElements.replace_indices_with_names(matrix, allLogFunctions)

        # Identify relationships and replace names
        inter_component_relationships = Instantiation.identify_components_and_functions_relationships(matrix_function_with_interaction, opt_chromosome)
        inter_component_relationships_named = Instantiation.replace_interdependencies_by_capella_element_names(inter_component_relationships, allLogFunctions['LogicalFunc_name'].tolist(), logicalComponents)
        
        log_component_interdependecies = Instantiation.replace_name_by_java_objects(inter_component_relationships_named, logicalComponents)
        
        if resulting_chromosomes is not None:
            # Process the resulting chromosomes
            resulting_chromosomes = RetrieveCapellaElements.randomly_select_row_if_more_one_optimal_result(resulting_chromosomes)
            resulting_chromosomes_transpose = resulting_chromosomes.transpose().rename(columns={0: "Logical Component Name"})
            #print(resulting_chromosomes_transpose.to_string())
            print('- Start replacing Capella elements name by its JavaObject')
            melted = RetrieveCapellaElements.melt_and_map_chromosomes(resulting_chromosomes, allLogFunctions)
            function_and_components_to_allocate = RetrieveCapellaElements.merge_data(melted, logicalComponents)
            
            return function_and_components_to_allocate, log_component_interdependecies,matrix_replaced
        
    @staticmethod
    def filter_interdependencies(log_component_interdependecies, functionalExchanges):
        
        log_component_interdependecies['FEJavaObject'] = log_component_interdependecies.apply(lambda _: [], axis=1)
        log_component_interdependecies['FEName'] = log_component_interdependecies.apply(lambda _: [], axis=1)
        for idx, fe_row in functionalExchanges.iterrows():
            for grp_idx, grp_row in log_component_interdependecies.iterrows():
                # Check if the SourceFunction and TargetFunction are in the respective lists
                if fe_row['SourceFunction'] in grp_row['SourceFunctionName'] and \
                   fe_row['TargetFunction'] in grp_row['TargetFunctionName']:
                    log_component_interdependecies.at[grp_idx, 'FEJavaObject'].append(fe_row['FunctionalExchangeJavaObject'])
                    log_component_interdependecies.at[grp_idx, 'FEName'].append(fe_row['FunctionalExchange_name'])
        for grp_idx, grp_row in log_component_interdependecies.iterrows():
            if len(grp_row['FEJavaObject']) == 1:
                log_component_interdependecies.at[grp_idx, 'FEJavaObject'] = grp_row['FEJavaObject'][0]
            if len(grp_row['FEName']) == 1:
                log_component_interdependecies.at[grp_idx, 'FEName'] = grp_row['FEName'][0]
        log_component_interdependecies['ComponentExchangeJavaObject'] = None        
        log_component_interdependecies['CECreatedName'] = None
        return log_component_interdependecies

    @staticmethod
    def get_component_interactions(lc):
        all_exchanges = []
        # Retrieve ComponentExchange with ComponentPort and its Source/target component
        for ce in lc.get_all_contents_by_type(ComponentExchange):
            if ce is not None:
                compExch_name = ce.get_name()
                # Retrieving source 
                if ce.get_source_port() and ce.get_target_port() is not None:
                    source_port = ce.get_source_port()
                    source_component = source_port.get_java_object().eContainer().getName()
                    # Retrieving target
                    target_port = ce.get_target_port()
                    target_component = target_port.get_java_object().eContainer().getName()
    
                    # Handle multiple FunctionalExchanges
                    fe_list = ce.get_allocated_functional_exchange()  # Assuming this returns a list
                    fe_names = [fe.get_name() for fe in fe_list]
                    
                    # Append the exchange information along with all allocated functional exchanges
                    all_exchanges.append({
                        'ComponentExchange_name': compExch_name,
                        'SourceComponent': source_component,
                        'ComponentPortSource': source_port.get_name(),
                        'TargetComponent': target_component,
                        'ComponentPortTarget': target_port.get_name(),
                        'CEJavaObject': ce,
                        'AllocatedFunctionalExchanges': fe_names  ,
                        'FExchangeJavaObject':fe_list 
                    })
        
        # Create a DataFrame from the list of dictionaries
        componentExchanges = pd.DataFrame(all_exchanges)
        return componentExchanges
    @staticmethod
    def filter_component_exchange_missed(componentExchanges, logical_and_functional_interdependencies):
        if not componentExchanges.empty:
            for row in logical_and_functional_interdependencies.itertuples():
                source = row.SourceComponentName
                target = row.TargetComponentName
                match = componentExchanges[
                    (componentExchanges['SourceComponent'] == source) & 
                    (componentExchanges['TargetComponent'] == target)
                ]
                if not match.empty:
                    match_row = match.iloc[0]
                    # Set the value of 'ComponentExchangeJavaObject' directly via .at[] accessor
                    logical_and_functional_interdependencies.at[row.Index, 'ComponentExchangeJavaObject'] = match_row['CEJavaObject']
                    logical_and_functional_interdependencies.at[row.Index, 'CECreatedName'] = match_row['ComponentExchange_name']
        else:
            logical_and_functional_interdependencies=logical_and_functional_interdependencies
        interdependencies_to_export=logical_and_functional_interdependencies[['SourceComponentName','TargetComponentName','SourceFunctionName','TargetFunctionName', 'ComponentExchangeName','FEName']].copy()
        interdependencies_to_export.rename(columns={"FEName": "FunctionalExchangeName"}, inplace=True)
        
        return logical_and_functional_interdependencies,interdependencies_to_export
    
    @staticmethod
    def filter_exchanges(component_exchanges, logical_and_functional_interdependencies):
        if not component_exchanges.empty:
            interdependencies = logical_and_functional_interdependencies
            exchanges = component_exchanges[['ComponentExchange_name', 'AllocatedFunctionalExchanges']]
            for index, row in interdependencies.iterrows():
                # The Component Exchange Created Name
                ce_created_name = row['CECreatedName']
                if pd.notna(ce_created_name):
                    exchange_row = exchanges[exchanges['ComponentExchange_name'] == ce_created_name].iloc[0]
                    allocated_exchanges = exchange_row['AllocatedFunctionalExchanges']
                    if not isinstance(allocated_exchanges, list):
                        allocated_exchanges = [allocated_exchanges]
                    fe_names = row['FEName'] if isinstance(row['FEName'], list) else [row['FEName']]
                    fe_java_objects = row['FEJavaObject'] if isinstance(row['FEJavaObject'], list) else [row['FEJavaObject']]
                    # Ensure there is a corresponding FEName for each FEJavaObject
                    if len(fe_names) == len(fe_java_objects):
                        fe_pairs = list(zip(fe_names, fe_java_objects))
                        # Check if all FEName are not in AllocatedFunctionalExchanges
                        if all(name not in allocated_exchanges for name in fe_names):
                            continue  
                        filtered_pairs = [(name, obj) for name, obj in fe_pairs if name not in allocated_exchanges]
                        filtered_fe_names, filtered_fe_java_objects = zip(*filtered_pairs) if filtered_pairs else ([], [])
                        interdependencies.at[index, 'FEName'] = list(filtered_fe_names)
                        interdependencies.at[index, 'FEJavaObject'] = list(filtered_fe_java_objects)
            interdependencies = interdependencies[interdependencies['FEName'].apply(lambda x: len(x) > 0)]
        else:
            interdependencies=logical_and_functional_interdependencies
        return interdependencies

    @staticmethod
    def create_allocations(function_and_components_to_allocate,function_exchange_to_allocate ):
        LogicalArchitectureHandler.allocateFunctionToLogicalComponent(function_and_components_to_allocate, model)
        LogicalArchitectureHandler.process_create_elements(function_exchange_to_allocate, model )
        
    @staticmethod
    def export_allocations_to_excel(matrix, file_name, fixed_width=40):
        sheet_name = 'LogicalArchitectureProposed'
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            matrix.to_excel(writer, sheet_name=sheet_name, index=True, header=True)
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            thin_border_side = Side(style=None)
            thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

            for col in range(1, len(matrix.columns) + 2):  
                header_cell = worksheet.cell(row=1, column=col)
                header_cell.alignment = Alignment(wrap_text=True, horizontal='center')
                header_cell.border = Border(left=Side(style='thick'), right=Side(style='thick'), top=Side(style='thick'), bottom=Side(style='thick'))
                worksheet.column_dimensions[get_column_letter(col)].width = fixed_width
            first_column_width = max(len(str(cell.value)) for cell in worksheet["A"]) + 2 
            worksheet.column_dimensions['A'].width = first_column_width
            cell_a1 = worksheet.cell(row=1, column=1)
            cell_a1.alignment = Alignment(horizontal='center', vertical='center')

            for row in worksheet.iter_rows(min_row=2, max_row=len(matrix) + 1, min_col=1, max_col=len(matrix.columns) + 1):
                for cell in row:
                    cell.border = thin_border
                    cell.alignment = Alignment(horizontal='left', wrap_text=True)
    
    @staticmethod 
    def integrate_and_reorder_matrix(resulting_chromosomes, matrix_function_with_interaction):
        # Ensure matrix_function_with_interaction is a DataFrame
        if isinstance(matrix_function_with_interaction, np.ndarray):
            matrix_function_with_interaction = pd.DataFrame(matrix_function_with_interaction)
    
        last_row_df = pd.DataFrame([resulting_chromosomes], columns=matrix_function_with_interaction.columns)
        original_index = matrix_function_with_interaction.index[-1] + 1
        matrix_with_chromosomes = pd.concat([matrix_function_with_interaction, last_row_df])
        sorting_index = matrix_with_chromosomes.iloc[-1].argsort()
        matrix_reordered = matrix_with_chromosomes.iloc[:-1, :].iloc[sorting_index, sorting_index]
        matrix_reordered = matrix_reordered.astype(object)
        # Fill diagonal values with F1, F2, F3, ...
        for i in range(len(matrix_reordered)):
            matrix_reordered.iloc[i, i] = f"F{i+1}"
        matrix_reordered = pd.concat([matrix_reordered, last_row_df])
        matrix_reordered.index = list(matrix_reordered.index[:-1]) + [original_index]
        return matrix_reordered

    @staticmethod
    def replace_last_row_values(matrix, allLogFunctions):

        comp_index_to_name = dict(zip(allLogFunctions['Comp_index'], allLogFunctions['LogicalComponent_name']))
        matrix = matrix.astype(object)
        last_row_index = matrix.index[-1]
        for col in matrix.columns:
            value = matrix.at[last_row_index, col]
            if value in comp_index_to_name:
                matrix.at[last_row_index, col] = comp_index_to_name[value]

        new_index = matrix.index[:-1].tolist() + ["LogicalComponentName"]
        matrix.index = new_index
    
        return matrix
    
    @staticmethod
    def replace_indices_with_names(matrix, allLogFunctions):

        func_index_to_name = dict(zip(allLogFunctions['Func_index'], allLogFunctions['LogicalFunc_name']))
        matrix.index = [func_index_to_name.get(x, x) for x in matrix.index]
        matrix.columns = [func_index_to_name.get(x, x) for x in matrix.columns]
    
        return matrix
    @staticmethod
    def set_cell_styles(worksheet, matrix, fixed_width):
        """Set styles for cells, including headers and column widths."""
        header_fill_color = PatternFill(start_color='EBF1DE', end_color='EBF1DE', fill_type='solid')
        logical_fill_color = PatternFill(start_color='C5D9F1', end_color='C5D9F1', fill_type='solid')
        for col in range(2, len(matrix.columns) + 2):
            header_cell = worksheet.cell(row=1, column=col)
            header_cell.fill = header_fill_color
            header_cell.alignment = Alignment(textRotation=90, wrap_text=True, horizontal='center', vertical='center')
            worksheet.column_dimensions[get_column_letter(col)].width = fixed_width
        
        for row in range(2, worksheet.max_row + 1):
            col_a_cell = worksheet.cell(row=row, column=1)
            col_a_cell.fill = header_fill_color

        
        for row in range(2, worksheet.max_row + 1):
            if worksheet.cell(row=row, column=1).value == "LogicalComponentName":
                worksheet.cell(row=row, column=1).fill = PatternFill(fill_type=None)
                for col in range(2, worksheet.max_column + 1):  # Corrected to exclude the +2
                    cell_log = worksheet.cell(row=row, column=col)
                    cell_log.fill = logical_fill_color
                    cell_log.alignment = Alignment(textRotation=90, wrap_text=True, horizontal='center', vertical='center')

        worksheet.cell(row=1, column=1).fill = PatternFill(fill_type=None)
        worksheet.column_dimensions['A'].width = max(len(str(cell.value)) for cell in worksheet["A"]) + 2
        worksheet.cell(row=1, column=1).alignment = Alignment(horizontal='center', vertical='center')

    @staticmethod
    def apply_border_and_alignment(worksheet):
        """Apply border and alignment to all cells."""
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                             top=Side(style='thin'), bottom=Side(style='thin'))
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
            for cell in row:
                cell.border = thin_border
                cell.alignment = Alignment(wrap_text=True, horizontal='left')

    @staticmethod
    def find_f_values(worksheet):
        """Find 'F' values in each column and return their indices."""
        last_row_idx = worksheet.max_row
        f_row_indices = {}
        for col in range(1, worksheet.max_column + 1):
            for row in range(2, last_row_idx):  # Exclude the last row
                cell_value = worksheet.cell(row=row, column=col).value
                if cell_value and 'F' in str(cell_value):
                    f_row_indices[col] = row
                    break
        return f_row_indices

    @staticmethod
    def apply_fill_for_component_groups(worksheet, logical_component_names, f_row_indices):
        """Apply the fill for each component group, skipping the first column if necessary."""
        fill_color = PatternFill(start_color='C5D9F1', end_color='C5D9F1', fill_type='solid')
        component_col_ranges = {}
        for col, component in enumerate(logical_component_names, start=1):
            if isinstance(component, str) and component.strip():
                component_col_ranges.setdefault(component.strip(), []).append(col)
        
        for component, cols in component_col_ranges.items():
            cols_with_f = [col for col in cols if col in f_row_indices]
            if not cols_with_f:
                continue  # Skip components with no 'F' values
            top_row_to_fill = min(f_row_indices[col] for col in cols_with_f)
            bottom_row_to_fill = max(f_row_indices[col] for col in cols_with_f)
            for col in cols:
                if col == 1:
                    continue
                for row in range(top_row_to_fill, bottom_row_to_fill + 1):
                    worksheet.cell(row=row, column=col).fill = fill_color


    @staticmethod
    def export_dsm_permutated_to_excel(matrix, file_name, fixed_width=10):
        """Main method to export DSM permutated to Excel, applying all formatting and fill logic."""
        sheet_name = 'DSM_Permutated'
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            matrix.to_excel(writer, sheet_name=sheet_name, index=True, header=True)
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            # Set cell styles
            RetrieveCapellaElements.set_cell_styles(worksheet, matrix, fixed_width)

            # Apply border and alignment to all cells
            RetrieveCapellaElements.apply_border_and_alignment(worksheet)

            # Find 'F' values in each column
            f_row_indices = RetrieveCapellaElements.find_f_values(worksheet)

            # Apply the fill for each component group
            last_row_idx = worksheet.max_row
            logical_component_names = [worksheet.cell(row=last_row_idx, column=col).value for col in range(1, worksheet.max_column + 1)]
            RetrieveCapellaElements.apply_fill_for_component_groups(worksheet, logical_component_names, f_row_indices)
            
            # Save changes to the workbook
            workbook.save(filename=file_name)