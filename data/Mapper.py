from data import Methods

methodString = []


def get_list_methods(methods):
    for classes in methods:
        for met in methods[classes]:
            methodString.append(met)
    return methodString

