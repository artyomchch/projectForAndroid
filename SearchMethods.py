from androguard import misc
from termcolor import cprint

import Methods

a, d, dx = misc.AnalyzeAPK("sa.apk")


def search_methods(type_methods):
    for i in type_methods:
        print("Use Class: ", i)
        try:
            use_class = False
            for meth in dx.classes[i].get_methods():
                for _, call, _ in meth.get_xref_from():
                    for methods in type_methods[i]:
                        if methods.__str__() == call.name:
                            use_class = True
                            cprint("found method: --> {}".format(call.name), "green")
            if not use_class:
                cprint("Class {} found, but no search methods found".format(i), "yellow")
            print("__________________________")
        except KeyError:
            cprint("Androguard not found class --> {}".format(i), "red")
            print("__________________________")


print("Input methods")
search_methods(Methods.input)
print()
print()
print()
print()
print("Output methods")
search_methods(Methods.output)
