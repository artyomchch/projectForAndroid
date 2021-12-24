import matplotlib.pyplot as plt
import networkx as nx
from androguard import misc
from androguard.core.analysis.analysis import ExternalMethod


def certificate(a):  # CERTIFICATE
    file = open('certificate' + '.txt', 'w')
    for cert in a.get_certificates():
        file.write("the sha1 fingerprint: " + str(cert.sha1) + "\n")  # the sha1 fingerprint
        file.write("the sha256 fingerprint: " + str(cert.sha256) + "\n")  # the sha256 fingerprint
        file.write("issuer: " + cert.issuer.human_friendly + "\n")  # issuer
        file.write("subject, usually the same: " + cert.subject.human_friendly + "\n")  # subject, usually the same
        file.write("hash algorithm: " + cert.hash_algo + "\n")  # hash algorithm
        file.write("Signature algorithm: " + cert.signature_algo + "\n")  # Signature algorithm
        file.write("Serial number: " + str(cert.serial_number) + "\n")  # Serial number
        file.write("The DER coded bytes of the certificate itself: " + str(
            cert.contents) + "\n")  # The DER coded bytes of the certificate itself
    file.close()


def permission(a):  # PERMISSION
    file = open('permission' + '.txt', 'w')
    for perm in a.get_permissions():
        file.write(perm + "\n")
    file.close()


def activities(a):  # ACTIVITIES
    file = open('activities' + '.txt', 'w')
    for acti in a.get_activities():
        file.write(acti + "\n")
    file.close()


def aboutApp(a):  # ABOUT APP
    file = open('aboutApp.txt', 'w', encoding='utf-8')
    file.write("package name: " + a.get_package() + "\n")
    file.write("app name: " + str(a.get_app_name()) + "\n")
    file.write("app icon: " + str(a.get_app_icon()) + "\n")
    file.write("android version code: " + str(a.get_androidversion_code()) + "\n")
    file.write("android version name: " + str(a.get_androidversion_name()) + "\n")
    file.write("minimum sdk version: " + str(a.get_min_sdk_version()) + "\n")
    file.write("maximum sdk version: " + str(a.get_max_sdk_version()) + "\n")
    file.write("target sdk version: " + str(a.get_target_sdk_version()) + "\n")
    file.write("effective target sdk version: " + str(a.get_effective_target_sdk_version()) + "\n")
    file.close()


def classes(dx):
    file = open('classes' + '.txt', 'w')
    file.write(str(dx.get_classes()))
    file.close()


def methods(dx):
    file = open('methods' + '.txt', 'w')
    for method in dx.get_methods():
        file.write("inside Method {} ".format(method.name) + ':' + '\n')
        for _, call, _ in method.get_xref_to():
            file.write("    calling -> {} -- {} -- descriptor:  {}".format(call.class_name, call.name,
                                                                           call.get_descriptor()) + '\n')
    file.close()


def graph():
    CFG = nx.DiGraph()

    for m in dx.find_methods(classname="Lkozlov/artyom/avitoweather/presentation/addcity/AddCityFragment;"):
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



a, d, dx = misc.AnalyzeAPK("avito.apk")

certificate(a)
print("Certificate save")
permission(a)
print("Permission save")
activities(a)
print("Activities save")
aboutApp(a)
print("About app save")
classes(dx)
print("Classes save")
methods(dx)
print("Methods save")
graph()
