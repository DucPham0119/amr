import penman
from penman.graph import Graph

def convert(text, dp):
    variables = dict()
    concepts = []
    relations = []

    count = 1
    top = ''
    for d in dp:
        # print(d)
        id = int(d[0])
        rel = d[7]
        token = d[1]+'-'+str(id)
        if rel != '_':
            head = int(d[6])
            if rel == 'Rel':
                variable = 'x0'
                id = int(dp[head - 1][0])
                token = dp[head - 1][1]+'-'+str(id)
                top = variable
            else:
                variable = 'x' + str(count)
            count += 1
            if token.isdigit():
                variables[id] = token
            else:
                concept = (variable, ':instance', token)
                variables[id] = variable
                concepts.append(concept)

            if head != id:
                relation = (head, rel, id)
                relations.append(relation)

    # print(concepts)
    # print(relations)
    # print(variables)
    nodes_and_edges = reduce_node_amr(concepts, relations, variables)
    graph = Graph(nodes_and_edges)
    graph = penman.encode(graph, top)
    amr = [text, graph]
    return amr


def reduce_node_amr(concepts, relations, variables):
    concepts, relations, variables = logical_node_amr(concepts, relations, variables)

    for i in range(len(relations)):
        head = relations[i][0]
        rel_type = relations[i][1]
        index = relations[i][2]
        # đang lỗi
        if isinstance(index, int):
            relations[i] = (variables[head], rel_type, variables[index])
        else:
            relations[i] = (variables[head], rel_type, index)

    return concepts + relations


def logical_node_amr(concepts, relations, variables):
    relations_remove = []

    for i in range(len(relations)):
        if relations[i][1] == 'polarity':
            relations_remove.append(relations[i])
            relations[i] = (relations[i][0], relations[i][1], '-')

    # transform head relation:
    for relation in relations_remove:
        id = relation[2]
        head = relation[0]
        for i in range(len(relations)):
            if relations[i][0] == id:
                relations[i] = (head, relations[i][1], relations[i][2])

        # print(variables[id])
        for concept in concepts:
            if concept[0] == variables[id]:
                concepts.remove(concept)

        del variables[id]

    # print('concepts = ', concepts)
    # print('relations = ', relations)
    # print('variables = ', variables)
    # print()
    return concepts, relations, variables
