import networkx as nx
from androguard import misc

G = nx.DiGraph()
G.add_edges_from([('A', 'B'), ('A', 'C'), ('C', 'B')])

pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black')
nx.draw_networkx_labels(G, pos)

# plt.show()

a, d, dx = misc.AnalyzeAPK("avito.apk")

classString = 'Lkozlov/artyom/avitoweather/presentation/addcity/AddCityFragment;'
# Landroidx/core/location/LocationManagerCompat;



for meth in dx.classes[classString].get_methods():
    orig_method = meth.get_method()
  #  print("Found Method --> {}".format(orig_method))

    print("inside method {}".format(meth.name))
    for _, call, _ in meth.get_xref_to():

        print("  calling -> {} -- {}".format(call.class_name, call.name))
for field in dx.find_fields(classname=classString):
    print("Field: {}".format(field.name))
    for _, meth2 in field.get_xref_read():
        print("  read in {} -- {}".format(meth2.class_name, meth2.name))
    for _, meth2 in field.get_xref_write():
        print("  write in {} -- {}".format(meth2.class_name, meth2.name))

print()
print()
print()
print()
print()
print()




# for meth in dx.classes[classString].get_methods():
#     print("usage of method {}".format(meth.name))
#     for _, call, _ in meth.get_xref_from():
#         print("  called by -> {} -- {}".format(call.class_name, call.name))
