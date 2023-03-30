import matplotlib.pyplot as plt
import networkx as nx

class Libs(object):
    
    dicc = {} 
    
    def __init__(self, expression=None) -> None:
        
        if expression is not None:
            self.expression = expression
            self.traduction = self.translation(self.expression)
            self.postfix = self.infixToPostfix(self.traduction)

    def translation(self,r):
        translation = []
        exp = [char for char in r]
        balance_score = 0
        for e in exp:
            if e == '?':
                chr = translation.pop()
                if chr == ')':
                    aux = [chr]
                    sign_sum = 0
                    while chr != '(' and sign_sum != -1:
                        chr = translation.pop()
                        if chr == ')':
                            sign_sum += 1
                        elif chr == '(':
                            sign_sum -= 1
                            
                        aux.insert(0,chr)
                    aux_str = ''.join(aux)
                    new_str = '('+str(aux_str)+'|ϕ)' #(x|ε)
                    translation.append(new_str)
                else:
                
                    new_str = '('+str(chr)+'|ϕ)'
                    translation.append(new_str)
                
            elif e == '+':
                chr = translation.pop()
                if chr == ')':
                    aux = [chr]
                    sign_sum = 0
                    while chr != '(' and sign_sum != -1:
                        chr = translation.pop()
                        if chr == ')':
                            sign_sum += 1
                        elif chr == '(':
                            sign_sum -= 1
                            
                        aux.insert(0,chr)
                    aux_str = ''.join(aux)
                    new_str = str(aux_str)+'('+str(aux_str)+'*)'
                    translation.append(new_str)
                else:
                    
                    new_str = str(chr)+'('+str(chr)+'*)'
                    translation.append(new_str)
            
            elif e == '.':
                self.dicc['ϰ'] = e
                e = 'ϰ'
                translation.append(e)
            
            elif e == 'ε':
                self.dicc['ϕ'] = e
                e = 'ϕ'
                translation.append(e)
            
            
            else:
                translation.append(e)
            
        string = ''.join(translation)
        
        # Balance verification
        for c in [char for char in string]:
            
            if c == '(':
                balance_score += 1
            elif c == ')':
                balance_score -= 1
            
        if balance_score != 0:
            print('---------------------------------------')
            print("ERROR: EXPRESIÓN DESBALANCEADA!!!")
            print('---------------------------------------')
            raise SystemExit
        
        return string

    def getPrecedence(self,c):
        precedence = ''

        if c == '(':
            precedence = 1
        elif c == '|':
            precedence = 2
        elif c == '.':
            precedence = 3
        elif (c == '*') or (c == '?') or (c == '+'):
            precedence = 4
        elif c == '^':
            precedence = 5
        else:
            precedence = 6

        return precedence

    def formatRegEx(self,regex):
        res = ''
        i = 0
        allOperators = ['|', '?', '+', '*', '^']
        binaryOperators = ['^', '|']
        for i in range(len(regex)):
            c1 = regex[i]
            if ((i + 1) < len(regex)):
                c2 = regex[i+1]
                res += c1
            
            if (c1 != '(') and (c2 != ')') and (c2 not in allOperators) and (c1 not in binaryOperators):
                try:
                    if res[-1] != '.':
                        res += '.'
                except:
                    pass
        res += regex[len(regex)-1]
        return res

    def infixToPostfix(self,regex):
        postfix = ''
        stack = []
        formattedRegEx = self.formatRegEx(regex)
        for c in formattedRegEx:
            if c == '(':
                stack.append(c)
            elif c == ')':
                try:
                    while stack[-1] != '(':
                        postfix += stack.pop()
                    stack.pop()
                except:
                    print('---------------------------------------')
                    print("ERROR: EXPRESIÓN DESBALANCEADA!!!")
                    print('---------------------------------------')
                    raise SystemExit
            else:
                while len(stack) > 0:
                    peekedChar = stack[-1]
                    peekedCharPrecedence = self.getPrecedence(peekedChar)
                    currentCharPrecedence = self.getPrecedence(c)

                    if peekedCharPrecedence >= currentCharPrecedence:
                        postfix += stack.pop()
                    else:
                        break
                
                stack.append(c)
        
        while len(stack) > 0:
            postfix += stack.pop()
        
        return postfix

    def get_postfix(self):
        return self.postfix
    
    def get_translation(self):
        return self.traduction
 
    def get_printable_trans(self):
        
        aux = ''
        for i in self.traduction:

            if i in self.dicc:
                i = self.dicc[i]
                aux += str(i)
            else:
                aux += str(i)
        return aux
    
    def get_printable_postfix(self):
        
        aux = ''
        for i in self.postfix:

            if i in self.dicc:
                i = self.dicc[i]
                aux += str(i)
            else:
                aux += str(i)
        return aux
    
class Nodes(object):

    def __init__(self, arg=None) -> None:
        
        if arg is not None:
            
            self.id = arg[0]
            self.status = arg[1]
    
    def set_id(self, new_id):
        
        self.id = new_id
        
    def set_status(self, new_status):
        
        self.status = new_status
         
class Edges(object):
    
    def __init__(self, arg=None) -> None:
        
        
        if arg is not None:
            
            self.local_init_node = Nodes()
            self.local_end_node = Nodes()
            
            self.local_init_node = arg[0]
            self.local_end_node = arg[1]
            self.trans_element = arg[2]

class Structures(object):

    def __init__(self) -> None:
        self.sub_transitions = []

        
    def append_edges(self,edge):
            
        self.sub_transitions.append(edge)
        
    def insert_edges(self, index, structure):
        self.sub_transitions.insert(index, structure)
    
class Transitions(object):

    transitions = []

    def __init__(self) -> None:
        pass
    
    def insert_transitions(self, structure):
        self.transitions.append(structure)
    
           
class NFA(object):  
    
    def __init__(self, postfix=None) -> None:
        if postfix is not None:
            self.postfix = postfix
    
    def find_last_index(self, index_list):
        
        return max(index_list)
         
    def thompson(self, postfix):
        iteration = len(postfix)
        nfa_stack = [char for char in postfix]
        trans = Transitions()
        li = Libs()
        last_node_index = 0
        last_index = 0
      

        for i in range(iteration):
            e = nfa_stack.pop(0)
            if e == '.':
                
                try: # If there is not another structure to concatenate --> pass
                    struct_1 = trans.transitions[-2].sub_transitions
                    struct_2 = trans.transitions[-1].sub_transitions
                    struct_1.extend(struct_2)
                    trans.transitions.pop()
                except:
                    pass
                
            elif e == '|':
                struct_1 = trans.transitions[-2]
                                
                try: # If there is not another structure to concatenate --> pass
                    struct_2 = trans.transitions[-1]
                except:
                    print("ERROR: No se encontró la segunda estructura!!!")
                    break
                
                last_struct1_index = struct_2.sub_transitions[0].local_init_node.id
                s1_index = [struct_1.sub_transitions[0].local_init_node.id, last_struct1_index]
                
                # Index modification for expecting concatenation
                
                index_list = []
                for i in range(len(struct_2.sub_transitions)):
                    # Getting & updating id from initial edge
                    current_id = struct_2.sub_transitions[i].local_init_node.id
                    original_init_node = current_id+1 # Original Init Node ID
                    struct_2.sub_transitions[i].local_init_node.set_id(original_init_node)
                    # Getting & updating id from ending edge
                    current_id = struct_2.sub_transitions[i].local_end_node.id
                    original_end_node = current_id+1
                    struct_2.sub_transitions[i].local_end_node.set_id(original_end_node)
                    index_list.append(original_end_node)
                
                last_struct2_node = self.find_last_index(index_list)
                
                s2_index = [struct_2.sub_transitions[0].local_init_node.id, last_struct2_node]
                
                # print(s1_index, s2_index)
                
                struct_1.sub_transitions.extend(struct_2.sub_transitions)
                trans.transitions.pop()
                
                # Purely last used index
                last_structure = trans.transitions[-1]
                last_index = 0
                #last_structure.sub_transitions.index(trans.transitions[-1].sub_transitions[0])
                # New init node ID
                init_node_index = last_structure.sub_transitions[last_index].local_init_node.id
                # Pre node epsilon
                pre_node_init = Nodes([init_node_index, "none"])
                pre_node_end = Nodes([init_node_index+1, "none"])
                pre_edge = Edges([pre_node_init, pre_node_end,'ε'])
                last_structure.insert_edges(0,pre_edge)
                
                # Updating ID nodes
                # Purely last used index
                last_index = 1
                #last_structure.sub_transitions.index(trans.transitions[-1].sub_transitions[1])
                for i in range(last_index, len(trans.transitions[-1].sub_transitions)):
                    # Getting & updating id from initial edge
                    current_id = last_structure.sub_transitions[i].local_init_node.id
                    original_init_node = current_id+1 # Original Init Node ID
                    last_structure.sub_transitions[i].local_init_node.set_id(original_init_node)
                    # Getting & updating id from ending edge
                    current_id = last_structure.sub_transitions[i].local_end_node.id
                    original_end_node = current_id+1
                    last_structure.sub_transitions[i].local_end_node.set_id(original_end_node)
                    
                    last_index = i
                    last_node_index = last_struct2_node+1
                    
                # Post node epsilon
                post_node_init = Nodes([last_node_index, "none"])
                post_node_end = Nodes([last_node_index+1, "none"])
                post_edge = Edges([post_node_init, post_node_end,'ε'])
                last_structure.append_edges(post_edge)
                
                
                # Extra ε transitions
                # epsilon struct_2 ending to final
                epsilon_init_node = Nodes([s2_index[0], "none"])
                epsilon_end_node = Nodes([last_node_index+1, "none"])
                init_end_edge = Edges([epsilon_init_node, epsilon_end_node,'ε'])
                last_structure.append_edges(init_end_edge)
                
                last_index += 1
                
                #epsilon start to struct
                epsilon_origin_init_node = Nodes([s1_index[0], "none"])
                epsilon_origin_end_node = Nodes([s2_index[0]+1, "none"])
                epsilon_origin_edge = Edges([epsilon_origin_init_node, epsilon_origin_end_node,'ε'])
                last_structure.append_edges(epsilon_origin_edge)
                
                last_node_index += 1
                                 
            elif e == '*':
                # Purely last used index
                last_structure = trans.transitions[-1]
                last_index = 0
                #last_structure.sub_transitions.index(trans.transitions[-1].sub_transitions[0])
                # New init node ID
                init_node_index = last_structure.sub_transitions[last_index].local_init_node.id
                # Pre node epsilon
                pre_node_init = Nodes([init_node_index, "none"])
                pre_node_end = Nodes([init_node_index+1, "none"])
                pre_edge = Edges([pre_node_init, pre_node_end,'ε'])
                last_structure.insert_edges(0,pre_edge)
                
                # Updating ID nodes
                # Purely last used index
                last_index = 1
                #last_structure.sub_transitions.index(trans.transitions[-1].sub_transitions[1])
                index_list = []
                for i in range(last_index, len(trans.transitions[-1].sub_transitions)):
                    # Getting & updating id from initial edge
                    current_id = last_structure.sub_transitions[i].local_init_node.id
                    original_init_node = current_id+1 # Original Init Node ID
                    last_structure.sub_transitions[i].local_init_node.set_id(original_init_node)
                    # Getting & updating id from ending edge
                    current_id = last_structure.sub_transitions[i].local_end_node.id
                    original_end_node = current_id+1
                    last_structure.sub_transitions[i].local_end_node.set_id(original_end_node)
                    index_list.append(original_end_node)
                    
                    last_index = i
                
                last_node_index =self.find_last_index(index_list)
                
                
                # last_node_index = current_id+1
                # last_index += 1
                
                # Post node epsilon
                post_node_init = Nodes([last_node_index, "none"])
                post_node_end = Nodes([last_node_index+1, "none"])
                post_edge = Edges([post_node_init, post_node_end,'ε'])
                last_structure.append_edges(post_edge)
                
                # last_node_index += 1
                # last_index += 1
                
                # Extra ε transitions
                # epsilon init-end node
                epsilon_init_node = Nodes([init_node_index, "none"])
                epsilon_end_node = Nodes([last_node_index+1, "none"])
                init_end_edge = Edges([epsilon_init_node, epsilon_end_node,'ε'])
                last_structure.append_edges(init_end_edge)
                
                last_index += 1
                
                #epsilon original edge
                epsilon_origin_init_node = Nodes([last_node_index, "none"])
                epsilon_origin_end_node = Nodes([init_node_index+1, "none"])
                epsilon_origin_edge = Edges([epsilon_origin_init_node, epsilon_origin_end_node,'ε'])
                last_structure.append_edges(epsilon_origin_edge)
                
                last_node_index += 1          
            
            else:
                
                init_node = Nodes([last_node_index, "none"])
                last_node_index += 1
                end_node = Nodes([last_node_index, "none"])
                trans_elem = e
                current_edge = Edges([init_node, end_node, trans_elem])
                structure = Structures()
                structure.append_edges(current_edge)
                trans.insert_transitions(structure)
                
        # Crear un nuevo gráfico de red vacío
        G = nx.DiGraph()

        
        end_node_id = []
        ind = -1
        for i in range(len(trans.transitions[ind].sub_transitions)):
            
            # print('Edge: ',i)
            
            self.AFN_transitions = trans.transitions[ind] 
            
            init_dg = self.AFN_transitions.sub_transitions[i].local_init_node.id            
            end_dg = self.AFN_transitions.sub_transitions[i].local_end_node.id
            elem_dg = self.AFN_transitions.sub_transitions[i].trans_element
            end_node_id.append(end_dg)
            if elem_dg in li.dicc:
                elem_dg = li.dicc[elem_dg]
                
            # print('Init Node: ',trans.transitions[ind].sub_transitions[i].local_init_node.id)
            # print('End Node: ',trans.transitions[ind].sub_transitions[i].local_end_node.id)
            print(str(init_dg)+' → ('+str(elem_dg)+') → '+str(end_dg)+',')
            
            
            # Agregar dos nodos al gráfico
            G.add_node(init_dg)
            G.add_node(end_dg)
            # Agregar una transición del nodo 0 al nodo 1 con el símbolo 'a'
            G.add_edge(init_dg, end_dg, label=elem_dg)
            
            # print('Transition Element: ',trans.transitions[ind].sub_transitions[i].trans_element)
            # print('.....................................')
        
        # Dibujar el gráfico
        
        
        self.set_initial_state(0)
        self.set_acceptance_state(self.find_last_index(end_node_id))

        # print('---------------------------')
        # print('INITIAL STATE:',trans.initial_state,'\nFINAL STATE:',trans.acceptance_state)
        # print('---------------------------')
        
        
        
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos)
        nx.draw_networkx_labels(G, pos)
        plt.show()

    def get_transitions(self):
        return self.AFN_transitions

    def set_initial_state(self, state):
        self.initial_state = state
    
    def get_initial_state(self):
        return self.initial_state
     
    def set_acceptance_state(self, state):
        self.acceptance_state = state

    def get_acceptance_state(self):
        return self.acceptance_state
    
    def get_standarized_trans(self):
        stand_trans = {}
        struct = self.get_transitions()
        for i in range(len(struct.sub_transitions)):
            init_dg = struct.sub_transitions[i].local_init_node.id            
            end_dg = struct.sub_transitions[i].local_end_node.id
            elem_dg = struct.sub_transitions[i].trans_element
            if not init_dg in stand_trans:
                stand_trans[init_dg] = {}
            stand_trans[init_dg][end_dg] = elem_dg 
            
        return stand_trans

