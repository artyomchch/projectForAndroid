import hashlib

import matplotlib.pyplot as plt
import networkx as nx
from androguard import misc
from androguard.core import bytecode
from androguard.core.analysis.analysis import ExternalMethod


def activities(a):  # ACTIVITIES
    file = open('../logs/activities' + '.txt', 'w')
    for acti in a.get_activities():
        file.write(acti + "\n")
    file.close()


def services(a):
    file = open('../logs/services' + '.txt', 'w')
    for serv in a.get_services():
        file.write(serv + "\n")
    file.close()


def providers(a):
    file = open('../logs/provides' + '.txt', 'w')
    for prod in a.get_providers():
        file.write(prod + "\n")
    file.close()


def permission(a):  # PERMISSION
    file = open('../logs/permission' + '.txt', 'w')
    for perm in a.get_permissions():
        file.write(perm + "\n")
    file.close()


def certificate(a):  # CERTIFICATE
    file = open('../logs/certificate' + '.txt', 'w')
    for cert in a.get_certificates():
        file.write("the sha1 fingerprint: " + str(hashlib.sha1(cert.sha1).hexdigest()) + "\n")  # the sha1 fingerprint
        file.write("the sha256 fingerprint: " + str(hashlib.sha256(cert.sha256).hexdigest()) + "\n")  # the sha256 fingerprint
        file.write("issuer: " + cert.issuer.human_friendly + "\n")  # issuer
        file.write("subject, usually the same: " + cert.subject.human_friendly + "\n")  # subject, usually the same
        file.write("hash algorithm: " + cert.hash_algo + "\n")  # hash algorithm
        file.write("Signature algorithm: " + cert.signature_algo + "\n")  # Signature algorithm
        file.write("Serial number: " + str(cert.serial_number) + "\n")  # Serial number
    # file.write("The DER coded bytes of the certificate itself: " + str(
    #     cert.contents) + "\n")  # The DER coded bytes of the certificate itself
    file.close()


def aboutApp(a):  # ABOUT APP
    file = open('../logs/aboutApp.txt', 'w', encoding='utf-8')
    file.write("package name: " + a.get_package() + "\n")
    file.write("app name: " + str(a.get_app_name()) + "\n")
    # file.write("app icon: " + str(a.get_app_icon()) + "\n")
    # file.write("android version code: " + str(a.get_androidversion_code()) + "\n")
    # file.write("android version name: " + str(a.get_androidversion_name()) + "\n")
    file.write("minimum sdk version: " + str(a.get_min_sdk_version()) + "\n")
    file.write("maximum sdk version: " + str(a.get_max_sdk_version()) + "\n")
    file.write("target sdk version: " + str(a.get_target_sdk_version()) + "\n")
    # file.write("effective target sdk version: " + str(a.get_effective_target_sdk_version()) + "\n")
    file.close()


def classes(dx):
    file = open('../logs/classes' + '.txt', 'w')
    file.write(str(dx.get_classes()))
    file.close()


def methods(dx):
    file = open('../logs/methods' + '.txt', 'w')
    for method in dx.get_methods():
        file.write("inside Method {} ".format(method.name) + ':' + '\n')
        for _, call, _ in method.get_xref_to():
            file.write("    calling -> {} -- {} -- descriptor:  {}".format(call.class_name, call.name,
                                                                           call.get_descriptor()) + '\n')
    file.close()


def intents(a):
    intent_filters = {}

    activities = a.get_activities()
    receivers = a.get_receivers()
    services = a.get_services()

    if activities is not None:
        for i in activities:
            filters = a.get_intent_filters("activity", i)
            if filters is not None and len(filters) > 0:
                intent_filters[i] = filters

    if receivers is not None:
        for i in receivers:
            filters = a.get_intent_filters("receiver", i)
            if filters is not None and len(filters) > 0:
                intent_filters[i] = filters

    if services is not None:
        for i in services:
            filters = a.get_intent_filters("service", i)
            if filters is not None and len(filters) > 0:
                intent_filters[i] = filters

    file = open('../logs/intents' + '.txt', 'w')
    for intent in intent_filters:
        file.write(intent + "\n")
    file.close()


def graph():
    CFG = nx.DiGraph()

    for m in dx.find_methods(classname="Landroidx/core/location/LocationManagerCompat;"):
        orig_method = m.get_method()
        print("Found Method --> {}".format(orig_method))
        # orig_method might be a ExternalMethod too...
        # so you can check it here also:
        if isinstance(orig_method, ExternalMethod):
            is_this_external = True

            # If this class is external, there will be very likely
            # no xref_to stored! If there is, it is probably a bug in androguard...
        else:
            is_this_external = False

        CFG.add_node(orig_method, external=is_this_external)

        for other_class, callee, offset in m.get_xref_to():
            if isinstance(callee, ExternalMethod):
                is_external = True
            else:
                is_external = False

            if callee not in CFG.node:
                CFG.add_node(callee, external=is_external)

            # As this is a DiGraph and we are not interested in duplicate edges,
            # check if the edge is already in the edge set.
            # If you need all calls, you probably want to check out MultiDiGraph
            if not CFG.has_edge(orig_method, callee):
                CFG.add_edge(orig_method, callee)

    pos = nx.spring_layout(CFG)

    internal = []
    external = []

    for n in CFG.nodes:
        if isinstance(n, ExternalMethod):
            external.append(n)
        else:
            internal.append(n)

    nx.draw_networkx_nodes(CFG, pos=pos, node_color='red', nodelist=internal)  # внутренний вызов метода
    nx.draw_networkx_nodes(CFG, pos=pos, node_color='blue', nodelist=external)  # внешний вызов метода
    nx.draw_networkx_edges(CFG, pos=pos, edgelist=CFG.edges, edge_color='black')
    nx.draw_networkx_labels(CFG, pos=pos, labels={x: "{} {}".format(x.get_class_name(), x.get_name()) for x in CFG.adj})

    #   plt.draw()
    plt.show()


def fields():
    # for i in dx.find_fields(classname='.*ContentValues', fieldname='', fieldtype='.*', accessflags='.*'):
    #     print(i)
    file = open('../logs/fields' + '.txt', 'w')
    # for field in dx.find_fields(classname='.*', fieldname='.*', fieldtype='.*', accessflags='.*'):
    for field in dx.find_strings(string='.*'):
        print(field)
    file.close()


def get_invoke_class():
    file = open('../logs/fields' + '.txt', 'w')

    if dx is not None:
        strings = dx.get_strings_analysis()
        for item in strings:
            file.write(str(item.encode('utf-8')) + "\n")
        # file.write("\n\n\n\n\n\n\n\n\n\n   FIRST \n\n\n\n\n\n\n\n\n\n\n\n\n")
        # for ext_class in dx.get_external_classes():
        #     file.write(str(ext_class.name + "\n"))
        # file.write("\n\n\n\n\n\n\n\n\n\n   SECOND \n\n\n\n\n\n\n\n\n\n\n\n\n")
        # for cls in dx.get_classes():
        #     for meth in cls.get_methods():
        #         method_name = meth.name
        #         mname = "METH_" + method_name + "_" + bytecode.FormatDescriptorToPython(meth.access) + "_" + bytecode.FormatDescriptorToPython(
        #             meth.descriptor)
        #         file.write(mname + "\n")
        #
        #     for field in cls.get_fields():
        #         mname = "FIELD_" + bytecode.FormatNameToPython(field.name)
        #         # with open(field_file, 'a') as f1:
        #         #     f1.write(mname)
        #         file.write(mname + "\n")


a, d, dx = misc.AnalyzeAPK("../apk/test_apk.apk")

certificate(a)
print("Certificate save")
permission(a)
print("Permission save")
activities(a)
print("Activities save")
aboutApp(a)
print("About app save")
intents(a)
print("Intents save")
providers(a)
print("Providers save")
services(a)
print("services save")
classes(dx)
print("Classes save")
methods(dx)
print("Methods save")
# fields()
print("Fields save")
# graph()
get_invoke_class()
