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
class LogicalArchitectureHandler:

    @staticmethod
    def allocateFunctionToLogicalComponent(function_and_components_to_allocate, model):
        if function_and_components_to_allocate is not None:
            for index, row in function_and_components_to_allocate.iterrows():
                function_to_allocate = row['LogicalFunc_name']
                component_to_allocate_to = row['Components_name']
    
                model.start_transaction()
                
                try:
                    cfa = ComponentFunctionalAllocation()
                    cfa.set_source_element(component_to_allocate_to)
                    cfa.set_target_element(function_to_allocate)
                    component_to_allocate_to.get_java_object().getOwnedFunctionalAllocation().add(cfa.get_java_object())
                    
                    print(" *Function ", function_to_allocate.get_name(), "allocated to ", component_to_allocate_to.get_name())
                
                except Exception as e:
                    # If something went wrong, we rollback the transaction and print the exception
                    model.rollback_transaction()
                    print("An error occurred:", e)
                    raise
                
                else:
                    model.commit_transaction()
    
            # Save the model after all allocations
            model.save()
    
        else:
            print("- Any allocation to do")
            model.save()
            
    @staticmethod
    def create_component_port(java_object, port_name, orientation):
        """
        Create a component port.

        :param java_object: The Java object associated with the component.
        :param port_name: The name of the port to be created.
        :param orientation: The orientation of the port (either "IN" or "OUT").
        :return: The created component port.
        """
        new_port = ComponentPort()
        new_port.set_name(port_name)
        new_port.set_port_kind("FLOW")
        new_port.set_port_orientation(orientation)
        java_object.get_java_object().getOwnedFeatures().add(new_port.get_java_object())
        return new_port

    @staticmethod
    def create_component_exchange(source_port, target_port, exchange_name, source_component_java_object):
        """
        Create a component exchange.

        :param source_port: The source port for the exchange.
        :param target_port: The target port for the exchange.
        :param exchange_name: The name of the exchange.
        :param source_component_java_object: The Java object associated with the source component.
        :return: The created component exchange.
        """
        new_exchange = ComponentExchange()
        new_exchange.set_name(exchange_name)
        new_exchange.set_source_port(source_port)
        new_exchange.set_target_port(target_port)
        new_exchange.set_exchange_kind("FLOW")
        source_component_java_object.get_java_object().getOwnedComponentExchanges().add(new_exchange.get_java_object())
        return new_exchange
    @staticmethod  
    def create_cefea(source, target):
        """
        Create a ComponentExchangeFunctionalExchangeAllocation between a ComponentExchange and FunctionalExchange.
    
        :param source: The source element Java object for the allocation.
        :param target: The target element Java object for the allocation.
        """
        cefea = ComponentExchangeFunctionalExchangeAllocation()
        cefea.set_source_element(source)
        cefea.set_target_element(target)
        source.get_java_object().getOwnedComponentExchangeFunctionalExchangeAllocations().add(cefea.get_java_object())
        
    @staticmethod
    def process_create_elements(grouped_df, model):
        if not grouped_df.empty:
            """
            Process the grouped dataframe and create the necessary elements.
    
            :param grouped_df: The dataframe containing the relationships.
            :param model: The model object.
            """
            model.start_transaction()
            try:
                for idx, row in grouped_df.iterrows():
                    if row['ComponentExchangeJavaObject'] ==None:
                        source_port = LogicalArchitectureHandler.create_component_port(row['SourceComponentJavaObject'], row['SourceComponentPortName'], "OUT")
                        target_port = LogicalArchitectureHandler.create_component_port(row['TargetComponentJavaObject'], row['TargetComponentPortName'], "IN")
                        new_exchange = LogicalArchitectureHandler.create_component_exchange(source_port, target_port, row['ComponentExchangeName'], row['SourceComponentJavaObject'])
                        print(f"* Created ComponentExchange from {row['SourceComponentName']} to {row['TargetComponentName']}")
        
                        # Handle multiple FEJavaObjects for creating ComponentExchangeFunctionalExchangeAllocation
                        fe_java_objects = row['FEJavaObject']
                        if not isinstance(fe_java_objects, list):
                            fe_java_objects = [fe_java_objects]
        
                        for fe_java_object in fe_java_objects:
                            LogicalArchitectureHandler.create_cefea(new_exchange, fe_java_object)
                        print(f"** Allocated Functional interaction {row['FEName']} to the Logical interaction '{row['ComponentExchangeName']}")
                    
                    else:
                        component_exchange=row['ComponentExchangeJavaObject']
                        fe_java_objects = row['FEJavaObject']
                        if not isinstance(fe_java_objects, list):
                            fe_java_objects = [fe_java_objects]
        
                        for fe_java_object in fe_java_objects:
                            LogicalArchitectureHandler.create_cefea(component_exchange, fe_java_object)
                        print(f"** Allocated Functional interaction {row['FEName']} to the Logical interaction '{row['ComponentExchangeName']}")
            except Exception as e:
                model.rollback_transaction()
                print(f"An error occurred: {e}")
                raise
            else:
                model.commit_transaction()
            model.save()
        else:
            print("- Any modifications to do in the model")




    