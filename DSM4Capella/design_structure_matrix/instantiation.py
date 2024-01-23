"""
/*********************************************************************
* Copyright (c) {December 2023} {Samares-Engineering} authors:[Mirna Ojeda, Sebastien Dube,Jean-Marie Gauthier, Yash Kethan]
*
* This program and the accompanying materials are made
* available under the terms of the Eclipse Public License 2.0
* which is available at https://www.eclipse.org/legal/epl-2.0/
*
* SPDX-License-Identifier: EPL-2.0
**********************************************************************/

"""

class GeneticAlgorithmDialog:
    # Define default values to display in GUI
    DEFAULT_INITIAL_POP_SIZE = 1000
    DEFAULT_MAX_NUM_GENERATIONS = 50
    DEFAULT_SURVIVOR_PERCENTAGE = 70
    DEFAULT_PARENT_PERCENTAGE = 20
    DEFAULT_POPULATION_MUTATION_PERCENTAGE = 70
    DEFAULT_GENE_MUTATION_PERCENTAGE = 30
    labelInitialPopSize = None
    txtInitialPopSize = None
    labelMaxNumGenerations = None
    txtMaxNumGenerations = None
    labelSurvivorPercentage = None
    txtSurvivorPercentage = None
    labelParentPercentage = None
    labelPopulationMutationPercentage = None
    labelPopulationMutationPercentage = None 
    labelGeneMutationPercentage = None
    txtGeneMutationPercentage = None
    dsmOption = None
    
    def build(self):
        self.dsmOption = createComboViewer(["DSM Analysis", "DSM Analysis + Optimization"])
        self.labelInitialPopSize = createLabel("Initial Population Size:", "1/2 <x");
        self.txtInitialPopSize = createText("2-4/2 o!");
        self.txtInitialPopSize.setText(str(self.DEFAULT_INITIAL_POP_SIZE))
        self.labelMaxNumGenerations = createLabel("Max Number of Generations:", "1/3 <x");
        self.txtMaxNumGenerations = createText("2-4/3 o!");
        self.txtMaxNumGenerations.setText(str(self.DEFAULT_MAX_NUM_GENERATIONS));
        self.labelSurvivorPercentage = createLabel("Survivor Percentage:", "1/4 <x");
        self.txtSurvivorPercentage = createText("2-4/4 o!");
        self.txtSurvivorPercentage.setText(str(self.DEFAULT_SURVIVOR_PERCENTAGE));
        self.labelParentPercentage = createLabel("Parent Percentage:", "1/5 <x");
        self.txtParentPercentage = createText("2-4/5 o!");
        self.txtParentPercentage.setText(str(self.DEFAULT_PARENT_PERCENTAGE));
        self.labelPopulationMutationPercentage = createLabel("Population Mutation Percentage:", "1/6 <x");
        self.txtPopulationMutationPercentage = createText("2-4/6 o!");
        self.txtPopulationMutationPercentage.setText(str(self.DEFAULT_POPULATION_MUTATION_PERCENTAGE));
        self.labelGeneMutationPercentage = createLabel("Gene Mutation Percentage:", "1/7 <x");
        self.txtGeneMutationPercentage = createText("2-4/7 o!");
        self.txtGeneMutationPercentage.setText(str(self.DEFAULT_GENE_MUTATION_PERCENTAGE));
        
        
    def evaluate(self, javaDialog):
        selectedOption = javaDialog.getData(self.dsmOption)
        DSM4CapellaOption = None
        if selectedOption == "DSM Analysis":
            print("DSM4Capella Logical Architecture Analysis executing...")
            DSM4CapellaOption= "Analysis"
        elif selectedOption == "DSM Analysis + Optimization":
            print("DSM4Capella Logical Architecture Analysis and Optimization executing...")
            DSM4CapellaOption= "Optimization"
        else:
            print("Invalid selection")
        return DSM4CapellaOption

    def validate_input(self, input_value, default_value, min_value, max_value):
        if min_value <= input_value <= max_value:
            return input_value
        else:
            print(f"Invalid input detected. Reverting to default value: {default_value}")
            return default_value


class GeneticAlgorithmInitialParameters:
    DEFAULT_INITIAL_POP_SIZE = 1000
    DEFAULT_MAX_NUM_GENERATIONS = 50
    DEFAULT_SURVIVOR_PERCENTAGE = 70
    DEFAULT_PARENT_PERCENTAGE = 20
    DEFAULT_POPULATION_MUTATION_PERCENTAGE = 70
    DEFAULT_GENE_MUTATION_PERCENTAGE = 30

    def __init__(self, initial_pop_size=None, max_num_generations=None, survivor_percentage=None, 
                 parent_percentage=None, population_mutation_percentage=None, gene_mutation_percentage=None):

        if any(param is None for param in [initial_pop_size, max_num_generations, survivor_percentage, 
                                            parent_percentage, population_mutation_percentage, gene_mutation_percentage]):
            self.set_default_values()
        else:
            valid = self.validate_parameters(
                initial_pop_size, max_num_generations, 
                survivor_percentage, parent_percentage, 
                population_mutation_percentage, gene_mutation_percentage
            )

            if valid:
                self.initial_pop_size = initial_pop_size
                self.max_num_generations = max_num_generations
                self.survivor_percentage = survivor_percentage
                self.parent_percentage = parent_percentage
                self.population_mutation_percentage = population_mutation_percentage
                self.gene_mutation_percentage = gene_mutation_percentage
            else:
                self.set_default_values()

    def set_default_values(self):
        self.initial_pop_size = self.DEFAULT_INITIAL_POP_SIZE
        self.max_num_generations = self.DEFAULT_MAX_NUM_GENERATIONS
        self.survivor_percentage = self.DEFAULT_SURVIVOR_PERCENTAGE
        self.parent_percentage = self.DEFAULT_PARENT_PERCENTAGE
        self.population_mutation_percentage = self.DEFAULT_POPULATION_MUTATION_PERCENTAGE
        self.gene_mutation_percentage = self.DEFAULT_GENE_MUTATION_PERCENTAGE
        print("Set default value as initial parameters for the Genetic Algorithm")

    def validate_parameters(self, initial_pop_size, max_num_generations, survivor_percentage, parent_percentage, population_mutation_percentage, gene_mutation_percentage):
        if initial_pop_size is not None and initial_pop_size < 0:
            print("WARNING ! Invalid initial population size. Must be > 0.")
            return False
        if max_num_generations is not None and max_num_generations < 0:
            print("WARNING !Invalid max number of generations. Must be > 0.")
            return False
        if survivor_percentage is not None and not (0 < survivor_percentage <= 100):
            print("WARNING !Invalid survivor percentage. Must be between 0 and 100.")
            return False
        if parent_percentage is not None and not (0 < parent_percentage <= 100):
            print("WARNING !Invalid parent percentage. Must be between 0 and 100.")
            return False
        if population_mutation_percentage is not None and not (0 < population_mutation_percentage <= 100):
            print("WARNING !Invalid population mutation percentage. Must be between 0 and 100.")
            return False
        if gene_mutation_percentage is not None and not (0 < gene_mutation_percentage <= 100):
            print("WARNING !Invalid gene mutation percentage. Must be between 0 and 100.")
            return False
        return True

    def print_parameters(self):
        print("The inputs values for the Genetic Algorithm are:")
        print(f"-Initial Population Size: {self.initial_pop_size}")
        print(f"-Max Number of Generations: {self.max_num_generations}")
        print(f"-Survivor Percentage: {self.survivor_percentage}")
        print(f"-Parent Percentage: {self.parent_percentage}")
        print(f"-Population Mutation Percentage: {self.population_mutation_percentage}")
        print(f"-Gene Mutation Percentage: {self.gene_mutation_percentage}")
        print("_________________________________________")


class Instantiation:
    @staticmethod
    def launch_ga(nb_functions, nb_modules, not_fixed_functions_indices, num_generations, population, gene_count,
                  parent_percentage, survivor_percentage, population_mutation_percentage, gene_mutation_percentage,
                  n2_data,not_fixed_components):
        
        start_time = time.time()

        # Initialize lists for logging
        population_evolution = [population.shape[0]]  # Get the initial size of the population
        generation_list = list(range(num_generations))
        minimum_coupling_list = []

        for generation in generation_list:
            # EVALUATION
            coupling_values_list, tf = GeneticAlgorithm.fitness_coupling(population.shape[0], nb_modules, nb_functions, population, n2_data)
            min_coupling_value = np.min(coupling_values_list)
            minimum_coupling_list.append(min_coupling_value)

            # SELECTION
            survivors = GeneticAlgorithm.select_mating_pool(population, coupling_values_list, survivor_percentage)
            if survivors.shape[0] < 3:
                # If number of survivors is less than 3, exit loop
                coupling_values_list, tf = GeneticAlgorithm.fitness_coupling(survivors.shape[0], nb_modules, nb_functions, survivors, n2_data)
                break

            # CROSSOVER OF SURVIVOR
            new_child_people = GeneticAlgorithm.crossover(survivors, parent_percentage)
            
            # MUTATE CHILDS
            mutated_child = GeneticAlgorithm.mutation(new_child_people, not_fixed_components, not_fixed_functions_indices,
                                         population_mutation_percentage, gene_mutation_percentage)

            # CHECK SURVIVOR & CHILD ACCORDING TO THE CONSTRAINT
            survivors, mutated_child = GeneticAlgorithm.check(survivors, mutated_child, nb_modules)

            # Update population
            parents_num = survivors.shape[0]
            offspring_num = mutated_child.shape[0]
            new_population = np.zeros(((parents_num + offspring_num), nb_functions))
            new_population[:parents_num, :] = survivors
            new_population[parents_num:, :] = mutated_child
            population = new_population

        elapsed_time = time.time() - start_time
        minimum_coupling = min(minimum_coupling_list)

        print(f"time elapsed: ----{elapsed_time:.2f}----")
        return elapsed_time, minimum_coupling, population_evolution, generation_list, survivors, coupling_values_list, tf
    @staticmethod
    def identify_not_fixed_function_indices(fix_fun_id, nb_functions):
        """Return indices of functions that are not fixed."""
        return np.setdiff1d(np.arange(nb_functions), fix_fun_id)

    @staticmethod
    def instantiation(nb_functions, nb_modules, fix_func_id, fix_module, not_fixed_functions_indices, 
                      gene_count, max_num_generations, survivor_percentage, parent_percentage,
                      population_mutation_percentage, gene_mutation_percentage, n2_data, 
                      function_names, initial_pop_size,not_fixed_components): 
    
        # Initialization of population and execution of the genetic algorithm
        population = GeneticAlgorithm.init_population(nb_modules, nb_functions, initial_pop_size, fix_func_id, fix_module,not_fixed_components)
        final_time, minimum_coupling, population_evolution, generation_list, survivors, copl_list, tf \
            = Instantiation.launch_ga(nb_functions, nb_modules, not_fixed_functions_indices, max_num_generations,
                                      population, gene_count, parent_percentage, survivor_percentage,
                                      population_mutation_percentage, gene_mutation_percentage, n2_data,not_fixed_components)
    
        # Log outputs and find the survivor with minimum coupling
        print('Solution Chromosomes:\n', survivors, '\nCoupling Values:\n', copl_list)
        min_copl_idx = np.argmin(copl_list)
        opt_chromosome = survivors[min_copl_idx]
        print('The ordered allocation of Component for each Function is:\n', opt_chromosome)
        # Convert the survivor numpy array to a DataFrame and map function and module IDs to names
        print("- Start replacing the Functions and Components Ids by its corresponding names")
        chromosomes = pd.DataFrame([opt_chromosome], columns=function_names)
        comp_index_to_name = logicalComponents.set_index('Comp_index')['LogicalComponent_name'].to_dict()
        # Replacing the values of the optimal chromosome
        replaced_chromosome = [comp_index_to_name.get(id, "Unknown") for id in opt_chromosome]
        # Replace the values in chromosomes DataFrame as well if needed
        chromosomes = pd.DataFrame([replaced_chromosome], columns=function_names)

        return chromosomes, opt_chromosome

    @staticmethod
    def run_algorithm_process(functionsToAllocate, logicalComponents, matrix_function_with_interaction, config: GeneticAlgorithmInitialParameters):

        # Print basic statistics
        nb_functions = len(functionsToAllocate['LogicalFunc_name'])
        nb_modules = len(logicalComponents['LogicalComponent_name'])
        
        print(f"Total functions: {nb_functions}")
        print(f"Total Logical Components: {nb_modules}")

        # Filter rows where functions are already allocated
        not_available_df = functionsToAllocate[functionsToAllocate['Allocation_Status'] == 'Not_Available']
        if not not_available_df.empty:
            print("\nConstraint of allocated Functions to be respected:\n", 
                  not_available_df[['LogicalFunc_name', 'Component_name']].to_string())

        # Set up fixed function and module lists
        fix_func_id = not_available_df['Func_index'].tolist()
        # Calculate the array of indices that can be changed by mutation
        not_fixed_functions_indices = Instantiation.identify_not_fixed_function_indices(fix_func_id, nb_functions)
       
        not_fixed_components = logicalComponents[logicalComponents['LogComponent_Java'].apply(lambda x: isinstance(x, LogicalComponent))]

        not_fixed_components = not_fixed_components['Comp_index'].tolist()
        not_fixed_components =sorted(not_fixed_components)

        # Start instantiation 
        print(' Start Algorithm iterations')
        resulting_chromosomes, opt_chromose = Instantiation.instantiation(
            nb_functions, nb_modules, fix_func_id, not_available_df['Component_index'].tolist(),
            not_fixed_functions_indices, 0, config.max_num_generations, config.survivor_percentage, 
            config.parent_percentage, config.population_mutation_percentage, config.gene_mutation_percentage, 
            matrix_function_with_interaction, functionsToAllocate['LogicalFunc_name'], config.initial_pop_size,not_fixed_components) 
        
        return resulting_chromosomes, opt_chromose

    @staticmethod
    def identify_components_and_functions_relationships(matrix_function_with_interaction, resulting_chromosomes):
        # This dictionary will store component relationships and the functions causing the relationship.
        component_relationships = {}
    
        # Number of functions.
        num_functions = len(resulting_chromosomes)
    
        for i in range(num_functions):
            # Component where function i is allocated.
            component_i = resulting_chromosomes[i]
    
            for j in range(num_functions):
                # If function i interacts with function j.
                if matrix_function_with_interaction[i][j] == 1.0:
                    # Component where function j is allocated.
                    component_j = resulting_chromosomes[j]
    
                    # Create a tuple for the component pair (this time without sorting).
                    component_pair = (component_i, component_j)
    
                    # Store the relationship and the functions causing it.
                    if component_pair not in component_relationships:
                        component_relationships[component_pair] = []
    
                    component_relationships[component_pair].append((i, j))
    
        # Filter out relationships within the same component
        inter_component_relationships = {key: val for key, val in component_relationships.items() if key[0] != key[1]}
        
        data = []
        for (src_component, tgt_component), function_pairs in inter_component_relationships.items():
            for src_func, tgt_func in function_pairs:
                data.append([src_component, tgt_component, src_func, tgt_func])
        
        inter_component_relationships_df = pd.DataFrame(data, columns=['SourceComponentName', 'TargetComponentName', 'SourceFunctionName', 'TargetFunctionName'])
        return inter_component_relationships_df
    
    @staticmethod
    def replace_interdependencies_by_capella_element_names(inter_component_relationships_df, function_names, component_names):
        component_names_dict = component_names.set_index('Comp_index')['LogicalComponent_name'].to_dict()
        
        # Replace the function indices with their names
        inter_component_relationships_df['SourceFunctionName'] = inter_component_relationships_df['SourceFunctionName'].apply(lambda idx: function_names[idx])
        inter_component_relationships_df['TargetFunctionName'] = inter_component_relationships_df['TargetFunctionName'].apply(lambda idx: function_names[idx])
        
        # Replace component indices with their names using the dictionary
        inter_component_relationships_df['SourceComponentName'] = inter_component_relationships_df['SourceComponentName'].apply(lambda idx: component_names_dict.get(idx, idx))
        inter_component_relationships_df['TargetComponentName'] = inter_component_relationships_df['TargetComponentName'].apply(lambda idx: component_names_dict.get(idx, idx))
    
        # Group by SourceComponent and TargetComponent and aggregate the other columns into lists
        grouped_df = inter_component_relationships_df.groupby(['SourceComponentName', 'TargetComponentName']).agg(list).reset_index()
    
        # Calculate enumeration for SourceComponentPort and TargetComponentPort for the grouped data
        grouped_df['SourceComponentPortName'] = grouped_df.apply(lambda row: f"CompPortOUT_{row.name + 1}", axis=1)
        grouped_df['TargetComponentPortName'] = grouped_df.apply(lambda row: f"CompPortIN_{row.name + 1}", axis=1)
    
        # Add the JavaObject columns
        grouped_df['SourceComponentJavaObject'] = None
        grouped_df['TargetComponentJavaObject'] = None
        # Fill 'ComponentExchangeName' by concatenating 'SourceComponentPortName' and 'TargetComponentPortName'
        grouped_df['ComponentExchangeName'] = grouped_df['SourceComponentName'] + '_to_' + grouped_df['TargetComponentName']

        return grouped_df
    @staticmethod
    def replace_name_by_java_objects(grouped_df, allLogFunctions):
        
        # Create a dictionary to map Component_name to Component_instance
        component_name_to_instance = dict(zip(allLogFunctions['LogicalComponent_name'], allLogFunctions['LogComponent_Java']))
        
        # Replace 'SourceComponentJavaObject' based on 'SourceComponent'
        for idx, row in grouped_df.iterrows():
            if row['SourceComponentName'] in component_name_to_instance:
                grouped_df.at[idx, 'SourceComponentJavaObject'] = component_name_to_instance[row['SourceComponentName']]
                
            if row['TargetComponentName'] in component_name_to_instance:
                grouped_df.at[idx, 'TargetComponentJavaObject'] = component_name_to_instance[row['TargetComponentName']]
        
        return grouped_df



