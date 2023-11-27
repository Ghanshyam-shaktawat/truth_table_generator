from django.shortcuts import render


def isWellFormed(P):
    bracketLevel = 0
    for c in P:
        if c == "(":
            bracketLevel += 1
        if c == ")":
            if bracketLevel == 0:
                return False
            bracketLevel -= 1
    return bracketLevel == 0


def parseNegation(P, truthValues):
    return not parseProposition(P, truthValues)


def parseConjunction(P, Q, truthValues):
    return parseProposition(P, truthValues) and parseProposition(Q, truthValues)


def parseDisjunction(P, Q, truthValues):
    return parseProposition(P, truthValues) or parseProposition(Q, truthValues)


def parseConditional(P, Q, truthValues):
    return (not parseProposition(P, truthValues)) or parseProposition(Q, truthValues)


def parseBiconditional(P, Q, truthValues):
    return parseProposition(P, truthValues) == parseProposition(Q, truthValues)


def parseProposition(P, truthValues):
    P = P.replace(" ", "")

    if not isWellFormed(P):
        return "Error"

    while P[0] == "(" and P[-1] == ")" and isWellFormed(P[1:len(P) - 1]):
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
            return parseConditional(P[0:i], P[i + 1:], truthValues)
        if P[i] == "↔" and bracketLevel == 0:
            return parseBiconditional(P[0:i], P[i + 1:], truthValues)

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "∨" and bracketLevel == 0:
            return parseDisjunction(P[0:i], P[i + 1:], truthValues)

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "∧" and bracketLevel == 0:
            return parseConjunction(P[0:i], P[i + 1:], truthValues)

    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "¬" and bracketLevel == 0:
            return parseNegation(P[i + 1:], truthValues)

def index(request):
    query = None
    truth_table_data = None

    if request.method == 'POST':
        query = request.POST.get('query')
        truthValues = {}
        for i in range(len(query)):
            if query[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                truthValues[query[i]] = True

        headers = list(truthValues.keys())
        headers.append(query)

        rows = []
        row_values = list(truthValues.values())
        row_values.append("T" if parseProposition(
            query, truthValues) else "F")
        rows.append(row_values)

        j = len(truthValues.values()) - 1
        while True in truthValues.values():
            variable = list(truthValues.keys())[j]
            truthValues[variable] = not truthValues[variable]

            if not truthValues[variable]:
                row_values = list(truthValues.values())
                row_values.append("T" if parseProposition(
                    query, truthValues) else "F")
                rows.append(row_values)
                j = len(truthValues.values()) - 1
            else:
                j -= 1

        truth_table_data = {'headers': headers, 'rows': rows}

    context = {'query': query, 'truth_table_data': truth_table_data}
    return render(request, 'core/index.html', context)
