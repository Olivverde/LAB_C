# Abrir archivo

from NFA_lab import *
class Lexer(object):

    def __init__(self) -> None:
        self.pre_exist_patterns = self.pre_fab()

    def pre_fab(self):
        patterns_ax = { "'A'-'Z'": [chr(i) for i in range(ord('A'), ord('Z')+1)],
                              "'a'-'z'": [chr(i) for i in range(ord('a'), ord('z')+1)],
                              "'0'-'9'": [chr(i) for i in range(ord('0'), ord('9')+1)]}
        for i in patterns_ax:
            patterns_ax[i] = [letra + "|" for letra in patterns_ax[i]]
            patterns_ax[i][-1] = patterns_ax[i][-1][0]
        return patterns_ax
        
    def pattern_xtension(self, raw_pattern, previus_pattern):
        
        section = raw_pattern
        if previus_pattern + "+" in raw_pattern:
            section = previus_pattern + "(" + previus_pattern + "*)"
        
        if "?" in raw_pattern:
            raw_deconst = [char for char in raw_pattern]
            aux_constr = []
            for e in raw_deconst:
                # Si identifica un ?
                if e == '?':
                    internal = ""
                    prev = aux_constr.pop()
                    # Identifica si es un ) o un ]
                    if prev == ")":
                        par_finder = ""
                        # Buscara todo lo que haya dentro del paréntesis
                        while par_finder != "(":
                            par_finder = aux_constr.pop()
                            if par_finder != "(":
                                internal = par_finder + internal
                        # Modificará el contenido extraído
                        internal = "(" + internal + "|" + "ε)"
                        aux_constr.append(internal)
                        
                    elif prev == "]":
                        
                        par_finder = ""
                        # Buscara todo lo que haya dentro del corchete
                        while par_finder != "[":
                            par_finder = aux_constr.pop()
                            if par_finder != "[":
                                internal = par_finder + internal
                        # Modificará el contenido extraído
                        internal = internal.split("'")
                        internal = ''.join(internal)
                        aux = ""
                        for k in internal:
                            aux += k + "|"
                        internal = aux
                        internal = "(" + internal + "ε)"
                        aux_constr.append(internal)
                       
                else:
                    aux_constr.append(e)
                
                section = ''.join(aux_constr)
        
        
        return section
          
    def pattern_translation(self, raw_pattern, patterns):
        pep = self.pre_exist_patterns
        aux_pattern = []
        section = ''
        # Si comienza con [ ] se los retira
        # if "'" in raw_pattern:
        #     raw_pattern = raw_pattern.replace("'","")
        if raw_pattern.startswith("[") and raw_pattern.endswith("]"):  
            raw_pattern = raw_pattern[1:-1]
            if raw_pattern.startswith('"') and raw_pattern.endswith('"'):
                raw_pattern = raw_pattern[1:-1]
                
                if '\\' in raw_pattern:
                    ax = ''
                    raw_pattern = [x for x in raw_pattern.split('\\') if x]
                    for e in range(len(raw_pattern)):
                        ax = ax + '\\' + raw_pattern[e]
                        if e != len(raw_pattern) - 1:   
                            ax = ax + '|'
                    raw_pattern = ax
                else:
                    ax = ''
                    for e in range(len(raw_pattern)):
                        ax = ax + raw_pattern[e]
                        if e != len(raw_pattern) - 1:   
                            ax = ax + '|'
                    raw_pattern = ax
            
            

            # Si identifica un patron pre-existente lo traduce
            for i in pep.keys():
                if i in raw_pattern:
                    raw_pattern = raw_pattern.replace(i,'')
                    if len(aux_pattern) != 0:
                        aux_pattern.append('|')
                        aux_pattern = aux_pattern + pep[i]
                    elif len(aux_pattern) == 0:
                        aux_pattern = aux_pattern + pep[i]
        # Si identifica una patrón participe dentro de otro patrón
        for j in patterns.keys():
            if j in raw_pattern:
                section = self.pattern_xtension(raw_pattern, j)
                return section
        
        if "'" in raw_pattern:
            raw_pattern = (raw_pattern.split("'"))
            aux = []
            for i in raw_pattern:
                if i != '':
                    aux.append(i)
                    aux.append('|')
            aux.pop()
            section = ''.join(aux)
            return section
        
        
        section = list(filter(None,raw_pattern.split("'")))
        section = section + aux_pattern
        
        section = ''.join(section)
        
        return section
    
    def reader(self, path):
        

        with open(path) as file:
            
            patterns = {}
            # Inicializar lista vacía
            let_vars = []
            # Leer archivo línea por línea
            for line in file:
                # Buscar "let" en la línea
                if 'let' in line:
                    # Obtener la variable después de "let" eliminando los espacios en blanco y el salto de línea
                    var = line.split("let ")[1].strip()
                    pattern_name = var.split("=")[0].strip()
                    pattern = var.split("=")[1].strip()
                    
                    pattern = self.pattern_translation(pattern, patterns)
                    
                    available_patterns = []
                    for l in patterns.keys():
                        if l in pattern:
                            available_patterns.append(l)
                    
                    for m in range(len(available_patterns)-1, -1, -1):
                        ava_aux = available_patterns[m]
                        pattern = pattern.replace(ava_aux, patterns[ava_aux])
                    
                    if "'" in pattern:
                        pattern = pattern.replace("'", '')
                    patterns[pattern_name] = pattern
            return patterns

    def afn_union(self, patterns):
        G = nx.DiGraph()
        afns = []
        for i in patterns:
            N = NFA()
            lib = Libs(patterns[i])
            postfix = lib.get_postfix()
            N.thompson(postfix)
            afns.append(N)
        
        lattest = 0
        for N in afns:

            init = N.get_initial_state()
            acceptance = N.get_acceptance_state()
            N.set_initial_state(init+1+lattest)
            N.set_acceptance_state(acceptance+1+lattest)

            for i in range(len(N.AFN_transitions.sub_transitions)):
                init_dg = N.AFN_transitions.sub_transitions[i].local_init_node.id            
                end_dg = N.AFN_transitions.sub_transitions[i].local_end_node.id
                elem_dg = N.AFN_transitions.sub_transitions[i].trans_element
                
                
                N.AFN_transitions.sub_transitions[i].local_init_node.set_id(init_dg+1+lattest)
                N.AFN_transitions.sub_transitions[i].local_end_node.set_id(end_dg+1+lattest)
                
                            
                init_dg = N.AFN_transitions.sub_transitions[i].local_init_node.id            
                end_dg = N.AFN_transitions.sub_transitions[i].local_end_node.id
                
                
                print(str(init_dg)+' → ('+str(elem_dg)+') → '+str(end_dg)+',')
                G.add_node(init_dg)
                G.add_node(end_dg)
                # Agregar una transición del nodo 0 al nodo 1 con el símbolo 'a'
                G.add_edge(init_dg, end_dg, label=elem_dg)
            
            
            
            init = N.get_initial_state()
            acceptance = N.get_acceptance_state()
            lattest = acceptance
            
            G.add_node(0)
            G.add_node(init)
            # Agregar una transición del nodo 0 al nodo 1 con el símbolo 'a'
            G.add_edge(0, init, label='ɛ')
            # print(init, acceptance) 
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos)
        nx.draw_networkx_labels(G, pos)
        plt.show()


path = 'inputs/slr-1.yal'
L = Lexer()
patterns  = L.reader(path)
L.afn_union(patterns)



