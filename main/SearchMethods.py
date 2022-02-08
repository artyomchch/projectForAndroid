from androguard import misc
from termcolor import cprint

from data import Methods, Mapper

a, d, dx = misc.AnalyzeAPK("../apk/avito.apk")

methodGenerationInput = []
methodGenerationOutput = []
permissionGeneration = []


def search_methods(type_methods, method_generation):
    for i in type_methods:
        print("Use Class: ", i)
        try:
            use_class = False
            for meth in dx.classes[i].get_methods():
                for _, call, _ in meth.get_xref_to():
                    for methods in type_methods[i]:
                        if methods == call.name:
                            use_class = True
                            cprint("found method: --> {}".format(call.name), "green")
                            method_generation.append(1)
            if not use_class:
                cprint("Class {} found, but no search methods found".format(i), "yellow")

                for k in range(len(type_methods[i])):
                    method_generation.append(0)
            print("__________________________")
        except KeyError:
            for k in range(len(type_methods[i])):
                method_generation.append(0)
            cprint("Androguard not found class --> {}".format(i), "red")
            print("__________________________")


print("Input methods")
search_methods(Methods.input, methodGenerationInput)
print("\n\n\n\n\n")
print("Output methods")
search_methods(Methods.output, methodGenerationOutput)

print(methodGenerationOutput)
print(methodGenerationInput)
print(Methods.output.keys())
print(Methods.input.keys())
print(dict(zip(Mapper.get_list_methods(Methods.output), methodGenerationOutput)))
