from django.shortcuts import render
from django.http import Http404

def is_well_formed(P):
    bracketLevel = 0
    for c in P:
        if c == "(":
            bracketLevel += 1
        if c == ")":
            if bracketLevel == 0:
                return False
            bracketLevel -= 1
    return bracketLevel == 0


def parse_negation(P, truthValues):
    return not parse_proposition(P, truthValues)


def parse_conjunction(P, Q, truthValues):
    return parse_proposition(P, truthValues) and parse_proposition(Q, truthValues)


def parse_disjunction(P, Q, truthValues):
    return parse_proposition(P, truthValues) or parse_proposition(Q, truthValues)


def parse_conditional(P, Q, truthValues):
    return (not parse_proposition(P, truthValues)) or parse_proposition(Q, truthValues)


def parse_biconditional(P, Q, truthValues):
    return parse_proposition(P, truthValues) == parse_proposition(Q, truthValues)


def parse_proposition(P, truthValues):
    P = P.replace(" ", "")

    if not is_well_formed(P):
        return "Error"

    while P[0] == "(" and P[-1] == ")" and is_well_formed(P[1:len(P) - 1]):
        P = P[1:len(P) - 1]

    if len(P) == 1:
        return truthValues[P]

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "→" and bracketLevel == 0:
            return parse_conditional(P[0:i], P[i + 1:], truthValues)
        if P[i] == "↔" and bracketLevel == 0:
            return parse_biconditional(P[0:i], P[i + 1:], truthValues)

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "∨" and bracketLevel == 0:
            return parse_disjunction(P[0:i], P[i + 1:], truthValues)

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "∧" and bracketLevel == 0:
            return parse_conjunction(P[0:i], P[i + 1:], truthValues)

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "¬" and bracketLevel == 0:
            return parse_negation(P[i + 1:], truthValues)

def index(request):
    query = None
    truth_table_data = None

    if request.method == 'POST':
        try:
            query = request.POST.get('query')
            truthValues = {}
            for i in range(len(query)):
                if query[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    truthValues[query[i]] = True

            headers = list(truthValues.keys())
            headers.append(query)

            rows = []
            row_values = list(truthValues.values())
            row_values.append("T" if parse_proposition(
                query, truthValues) else "F")
            rows.append(row_values)

            j = len(truthValues.values()) - 1
            while True in truthValues.values():
                variable = list(truthValues.keys())[j]
                truthValues[variable] = not truthValues[variable]

                if not truthValues[variable]:
                    row_values = list(truthValues.values())
                    row_values.append("T" if parse_proposition(
                        query, truthValues) else "F")
                    rows.append(row_values)
                    j = len(truthValues.values()) - 1
                else:
                    j -= 1

            truth_table_data = {'headers': headers, 'rows': rows}

        except IndexError:
            raise Http404("Error Query!")
            
        except KeyError:
            raise Http404("Query should be in proper format!")

    context = {'query': query, 'truth_table_data': truth_table_data}
    return render(request, 'core/index.html', context)
