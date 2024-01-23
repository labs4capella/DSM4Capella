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
from __future__ import annotations
    
# Extend the Logical architecture 
class LogicalComponent(LogicalComponent):  
    def get_allocated_logical_functions(self) -> List[LogicalFunction]:
        """
        Returns: List[LogicalFunction]
        """
        values = None
        if isinstance(self, LogicalComponent):
            values = self.get_java_object().getAllocatedLogicalFunctions()
    
        if not values:
            return []
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            return [e_object_class.get_class(value)(value) for value in values]
        
    def get_sub_logical_components(self):
        """
        Returns: LogicalComponents[*]
        """
        return create_e_list(self.get_java_object().getSubLogicalComponents(), LogicalComponent)
    
    def get_owned_features(self) -> List[Feature]:
        """
        Returns: ComponentPorts[*]
        """
        return create_e_list(self.get_java_object().getOwnedFeatures(), Feature)
    
class LogicalFunctionPkg(LogicalFunctionPkg):
    def get_allocating_logical_component(self) -> List[LogicalComponent]:
        """
        Returns: LogicalComponent[*]
        """
        return create_e_list(self.get_java_object().getAllocatingLogicalComponents(), LogicalComponent)   
     
class LogicalActor(LogicalActor):
    def get_allocated_logical_functions(self) -> List[LogicalFunction]:
        """
        Returns: List[LogicalFunction]
        """
        values = None
        if isinstance(self, LogicalActor):
            values = self.get_java_object().getAllocatedLogicalFunctions()
    
        if not values:
            return []
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            return [e_object_class.get_class(value)(value) for value in values]
    def get_owned_features(self) -> List[Feature]:
        """
        Returns: ComponentPort[*]
        """
        return create_e_list(self.get_java_object().getOwnedFeatures(), Feature)   
    
class LogicalFunction(LogicalFunction):
    def get_children_logical_functions(self):
        """
        Returns: LogicalFunction[*]
        """
        return create_e_list(self.get_java_object().getChildrenLogicalFunctions(), LogicalFunction)
    
#extend Ports 

class Port(CapellaElement):

    e_class = get_e_classifier("http://www.polarsys.org/capella/core/information/" + capella_version(), "Port")
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object_from_e_classifier(self.e_class))
        elif isinstance(java_object, Port):
            JavaObject.__init__(self, java_object.get_java_object())
        elif self.e_class.isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))

    def get_incoming_port_allocation(self) -> PortAllocation:
        """
        Returns: IncommingPort
        """
        value =  self.get_java_object().getIncomingPortAllocations()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
    def get_outgoing_port_allocation(self) -> List[PortAllocation]:
        """
        Returns: OutgoingPortAllocation[*]
        """
        return create_e_list(self.get_java_object().getOutgoingPortAllocations(), PortAllocation)

class PortAllocation(CapellaElement):

    e_class = get_e_classifier("http://www.polarsys.org/capella/core/information/" + capella_version(), "PortAllocation")
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object_from_e_classifier(self.e_class))
        elif isinstance(java_object, PortAllocation):
            JavaObject.__init__(self, java_object.get_java_object())
        elif self.e_class.isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
    
    def get_allocated_port(self) -> Port:
        """
        Returns: AllocatedPort
        """
        value =  self.get_java_object().getAllocatedPort()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def set_allocated_port(self, value: Port):
        """
        Parameters: value: FunctionPort
        """
        return self.get_java_object().setAllocatedPort(value.get_java_object())
    
    def get_allocating_port(self) -> Port:
        """
        Returns: ComponentPort
        """
        value =  self.get_java_object().getAllocatingPort()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def set_allocating_port(self, value: Port):
        """
        Parameters: value: ComponentPort
        """
        return self.get_java_object().setAllocatingPort(value.get_java_object())
    
# Extend Traces
class CapellaElement(CapellaElement):
    def get_owned_trace(self):
        value =  self.get_java_object().getOwnedTraces()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_contained_generic_trace(self):
        value =  self.get_java_object().getContainedGenericTraces()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_owned_traces(self):
        return create_e_list(self.get_java_object().getOwnedTraces(), Trace) 
    
    def get_contained_generic_traces(self):
        return create_e_list(self.get_java_object().getContainedGenericTraces(), GenericTrace)

#Extend allocations
  
class AbstractFunctionalBlock(CapellaElement):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/fa/" + capella_version(), "AbstractFunctionalBlock"))
        elif isinstance(java_object, AbstractFunctionalBlock):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/fa/" + capella_version(), "AbstractFunctionalBlock").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
        
    def get_owned_functional_allocation(self):
        value =  self.get_java_object().getOwnedFunctionalAllocation()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_functional_allocation(self):
        value =  self.get_java_object().getFunctionalAllocations()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_allocated_functions(self):
        value =  self.get_java_object().getAllocatedFunctions()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
           
    def get_owned_functional_allocations(self):
        return create_e_list(self.get_java_object().getOwnedFunctionalAllocation(), ComponentFunctionalAllocation)
    
    def get_functional_allocations(self):
        return create_e_list(self.get_java_object().getFunctionalAllocations(), ComponentFunctionalAllocation)

class TraceableElement(CapellaElement):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/common/core" + capella_version(), "TraceableElement"))
        elif isinstance(java_object, TraceableElement):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/common/core" + capella_version(), "TraceableElement").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
   
    def get_incoming_traces(self):

        value =  self.get_java_object().getIncomingTraces()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def set_incoming_traces(self, value):
        return self.get_java_object().setIncomingTraces(value.get_java_object())
    
    def get_outgoing_traces(self):
        value =  self.get_java_object().getOutgoingTraces()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def set_outgoing_traces(self, value):
        return self.get_java_object().setOutgoingTraces(value.get_java_object())  
       
    def get_incoming_trace(self):
        return create_e_list(self.get_java_object().getIncomingTraces(), AbstractTrace)
    
    def get_outgoing_trace(self):
        return create_e_list(self.get_java_object().getOutgoingTraces(), AbstractTrace)

class AbstractTrace(TraceableElement):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/common/core" + capella_version(), "AbstractTrace"))
        elif isinstance(java_object, AbstractTrace):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/common/core" + capella_version(), "AbstractTrace").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
    def get_source_element(self):
        value =  self.get_java_object().getSourceElement()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def set_source_element(self, value):
        return self.get_java_object().setSourceElement(value.get_java_object())
    
    def get_target_element(self):
        value =  self.get_java_object().getTargetElement()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def set_target_element(self, value):
        return self.get_java_object().setTargetElement(value.get_java_object())
    
    def get_target_element_trace(self):
        return create_e_list(self.get_java_object().getTargetElement(), TraceableElement) 
       
    def get_source_element_trace(self):
        return create_e_list(self.get_java_object().getSourceElement(), TraceableElement)  

class AbstractRelationship(CapellaElement):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/common/core" + capella_version(), "AbstractRelationship"))
        elif isinstance(java_object, AbstractRelationship):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/common/core" + capella_version(), "AbstractRelationship").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
    def get_realized_flow(self):
        value =  self.get_java_object().getRealizedFlow()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value) 
        
    def get_realized_flows(self):
        return create_e_list(self.get_java_object().getRealizedFlow(), AbstractInformationFlow)   
    
    def get_owned_traces(self):
        return create_e_list(self.get_java_object().getOwnedTraces(), Trace)
    
class AbstractInformationFlow(AbstractRelationship, CapellaElement):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/common/core" + capella_version(), "AbstractInformationFlow"))
        elif isinstance(java_object, AbstractInformationFlow):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/common/core" + capella_version(), "AbstractInformationFlow").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
    def get_realization(self):
        value =  self.get_java_object().getRealizations()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value) 
        
    def get_source(self):
        value =  self.get_java_object().getSource()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_target(self):
        value =  self.get_java_object().getTarget()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_realizations(self):
        return create_e_list(self.get_java_object().getRealizations(), AbstractRelationship)
                                      
class Relationship(AbstractRelationship,CapellaElement):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/core/" + capella_version(), "Relationship"))
        elif isinstance(java_object, Relationship):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/core/" + capella_version(), "Relationship").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
        
    def get_owned_traces(self):
        return create_e_list(self.get_java_object().getOwnedTraces(), Trace)
    

class Allocation(Relationship,AbstractTrace):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/core/" + capella_version(), " Allocation"))
        elif isinstance(java_object, Allocation):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/core/" + capella_version(), " Allocation").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
        
class AbstractFunctionAllocation(Allocation):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/fa/" + capella_version(), "AbstractFunctionAllocation"))
        elif isinstance(java_object, AbstractFunctionAllocation):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/fa/" + capella_version(), "AbstractFunctionAllocation").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
        
class ComponentFunctionalAllocation(AbstractFunctionAllocation):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/fa/" + capella_version(), "ComponentFunctionalAllocation"))
        elif isinstance(java_object, ComponentFunctionalAllocation):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/fa/" + capella_version(), "ComponentFunctionalAllocation").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))

    def get_function(self):
        value =  self.get_java_object().getFunction()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)

    def get_block(self):
        value =  self.get_java_object().getBlock()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)

    def get_function_abstract(self):
        return create_e_list(self.get_java_object().getFunction(), AbstractFunction)
    
    def get_block_abstract(self):
        return create_e_list(self.get_java_object().getBlock(), AbstractFunctionalBlock)

class Trace(Relationship, AbstractTrace):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/core" + capella_version(), "Trace"))
        elif isinstance(java_object, Trace):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/core" + capella_version(), "Trace").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object)) 


class GenericTrace(Trace):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/common/" + capella_version(), "GenericTrace"))
        elif isinstance(java_object, GenericTrace):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/common/" + capella_version(), "GenericTrace").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))

    def get_source(self):
        value =  self.get_java_object().getSource()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)

    def set_source(self, source):
        self.get_java_object().setSource(source.get_java_object())

    def get_target(self):
        value =  self.get_java_object().getTarget()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)

    def set_target(self, target):
        self.get_java_object().setTarget(target.get_java_object())
        
    def get_sources(self):
        return create_e_list(self.get_java_object().getSource(), TraceableElement) 
     
    def get_targets(self):
        return create_e_list(self.get_java_object().getTarget(), TraceableElement)


class TransfoLink(GenericTrace):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/common/" + capella_version(), "TransfoLink"))
        elif isinstance(java_object, TransfoLink):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/common/" + capella_version(), "TransfoLink").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))

class JustificationLink(GenericTrace):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/common/" + capella_version(), "JustificationLink"))
        elif isinstance(java_object, JustificationLink):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/common/" + capella_version(), "JustificationLink").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))

class AbstractFunction( AbstractEvent,CapellaElement):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/fa/" + capella_version(), "AbstractFunction"))
        elif isinstance(java_object, AbstractFunction):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/fa/" + capella_version(), "AbstractFunction").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))
   
    def get_allocations_blocks(self):
        value =  self.get_java_object().getAllocationBlocks()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_component_functional_allocations(self):
        value =  self.get_java_object().getComponentFunctionalAllocations()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_owned_functional_exchanges(self):
        value =  self.get_java_object().getOwnedFunctionalExchanges()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_owned_function(self):
        value =  self.get_java_object().getOwnedFunctions()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def get_component_functional_allocation(self):
        return create_e_list(self.get_java_object().getComponentFunctionalAllocations(), ComponentFunctionalAllocation)

    def get_owned_traces(self):
        return create_e_list(self.get_java_object().getOwnedTraces(), Trace)
    
    def get_owned_interactions(self):
        return create_e_list(self.get_java_object().getOwnedFunctionalExchanges(), Interaction)
    
    def get_owned_functions(self):
        return create_e_list(self.get_java_object().getOwnedFunctions(), OperationalActivity)
    
#Extend Component Ports
class Feature(CapellaElement):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/core" + capella_version(), "Feature"))
        elif isinstance(java_object, Feature):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/core" + capella_version(), "Feature").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object)) 
        
class Classifier(CapellaElement):
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object("http://www.polarsys.org/capella/core/core" + capella_version(), "Classifier"))
        elif isinstance(java_object, Classifier):
            JavaObject.__init__(self, java_object.get_java_object())
        elif get_e_classifier("http://www.polarsys.org/capella/core/core" + capella_version(), "Classifier").isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object)) 
    def get_owned_features(self) -> List[Feature]:
        """
        Returns: ComponentPorts[*]
        """
        return create_e_list(self.get_java_object().getOwnedFeatures(), Feature)  
     
class ComponentPort(ComponentPort):
    def get_kind(self) -> str:
        """
        Returns: String
        """
        value =  self.get_java_object().getKind()
        if value is None:
            return value
        else:
            return value.getName()
    
    VALID_KINDS = ["STANDARD", "FLOW"]
    def set_port_kind(self, kind: str) -> None:
        
        if kind not in self.VALID_KINDS:
            raise ValueError(f"'{kind}' is not a valid ComponentPortKind. Valid kinds are: {', '.join(self.VALID_KINDS)}")

        kind_enum_value = get_enum_literal("http://www.polarsys.org/capella/core/fa/" + capella_version(), 
                                           "ComponentPortKind", kind)
        self.get_java_object().setKind(kind_enum_value)
        
    VALID_ORIENTATIONS = ["UNSET", "IN","OUT", "INOUT"]
    def set_port_orientation(self, orientation: str) -> None:
        
        if orientation not in self.VALID_ORIENTATIONS:
            raise ValueError(f"'{orientation}' is not a valid OrientationPortKind. Valid orientations are: {', '.join(self.VALID_ORIENTATIONS)}")

        orientation_enum_value = get_enum_literal("http://www.polarsys.org/capella/core/fa/"  + capella_version(), 
                                           "OrientationPortKind", orientation)
        self.get_java_object().setOrientation(orientation_enum_value) 
        
class ComponentExchangeFunctionalExchangeAllocation(AbstractFunctionAllocation,CapellaElement):

    e_class = get_e_classifier("http://www.polarsys.org/capella/core/fa/" + capella_version(), "ComponentExchangeFunctionalExchangeAllocation")
    def __init__(self, java_object = None):
        if java_object is None:
            JavaObject.__init__(self, create_e_object_from_e_classifier(self.e_class))
        elif isinstance(java_object, ComponentExchangeFunctionalExchangeAllocation):
            JavaObject.__init__(self, java_object.get_java_object())
        elif self.e_class.isInstance(java_object):
            JavaObject.__init__(self, java_object)
        else:
            raise AttributeError("Passed object is not compatible with " + self.__class__.__name__ + ": " + str(java_object))

    def get_allocated_functional_exchange(self) -> FunctionalExchange:
        """
        Returns: FunctionalExchange
        """
        value =  self.get_java_object().getAllocatedFunctionalExchange()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
class ComponentExchange(ComponentExchange):
    def get_owned_component_exchange_ends(self) -> List[ComponentExchangeEnd]:
        """
        Returns: ComponentExchange[*]
        """
        return create_e_list(self.get_java_object().getOwnedComponentExchangeEnds(), ComponentExchangeEnd)

    def get_source_port(self) -> Port:
        """
        Returns: ComponentPort
        """
        value =  self.get_java_object().getSourcePort()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
    def get_target_port(self) -> Port:
        """
        Returns: ComponentPort
        """
        value =  self.get_java_object().getTargetPort()
        if value is None:
            return value
        else:
            e_object_class = getattr(sys.modules["__main__"], "EObject")
            specific_cls = e_object_class.get_class(value)
            return specific_cls(value)
        
    def set_source_port(self, value):
        return self.get_java_object().setSource(value.get_java_object())
    
    def set_target_port(self, value):
        return self.get_java_object().setTarget(value.get_java_object())
    
    VALID_KINDS = ["UNSET", "DELEGATION", "ASSEMBLY", "FLOW"]
    def set_exchange_kind(self, kind: str) -> None:
        
        if kind not in self.VALID_KINDS:
            raise ValueError(f"'{kind}' is not a valid ComponentExchangeKind. Valid kinds are: {', '.join(self.VALID_KINDS)}")

        kind_enum_value = get_enum_literal("http://www.polarsys.org/capella/core/fa/" + capella_version(), 
                                           "ComponentExchangeKind", kind)
        self.get_java_object().setKind(kind_enum_value) 
         
    def get_owned_component_exchange_functional_exchange_allocation(self)-> List[ComponentExchangeFunctionalExchangeAllocation]:
        """
        Returns: FunctionalExchange[*]
        """
        return create_e_list(self.get_java_object().getOwnedComponentExchangeFunctionalExchangeAllocations(), ComponentExchangeFunctionalExchangeAllocation)
    
    def get_allocated_functional_exchange(self)-> List[FunctionalExchange]:
        """
        Returns: FunctionalExchange[*]
        """
        return create_e_list(self.get_java_object().getAllocatedFunctionalExchanges(), FunctionalExchange)
    
class Interaction(Interaction):
    def get_owned_incoming_trace(self):
        """
        Returns: IncomingGenericTrace[*]
        """
        return create_e_list(self.get_java_object().getIncomingTraces(), GenericTrace)
    def get_owned_outgoing_trace(self):
        """
        Returns: OutgoingGenericTrace[*]
        """
        return create_e_list(self.get_java_object().getOutgoingTraces(), GenericTrace)
 
    def get_owned_traces(self):
        return create_e_list(self.get_java_object().getOwnedTraces(), Trace)
    
    def get_sources(self):
        """
        Returns: OperationalActivity[*]
        """
        return create_e_list(self.get_java_object().getSource(), Interaction)
    
    def get_targets(self):
        """
        Returns: OperationalActivity[*]
        """
        return create_e_list(self.get_java_object().getTarget(), Interaction)