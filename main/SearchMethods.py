import hashlib

from androguard import misc
from pymongo import MongoClient
from termcolor import cprint

a, d, dx = misc.AnalyzeAPK("../apk/avito.apk")

activity = []

methodGenerationInput = []
methodGenerationOutput = []
permissionGeneration = []
intent_filters = {}


def activities(a): return a.get_activities()  # ACTIVITIES


def providers(a): return a.get_providers()  # PROVIDERS


def services(a): return a.get_services()  # SERVICES


def permission(a): return a.get_permissions()  # PERMISSIONS


def aboutApp(a):  # ABOUT APP
    file = open('../logs/aboutApp.txt', 'w', encoding='utf-8')
    file.write("package name: " + a.get_package() + "\n")
    file.write("app name: " + str(a.get_app_name()) + "\n")
    file.write("minimum sdk version: " + str(a.get_min_sdk_version()) + "\n")
    file.write("maximum sdk version: " + str(a.get_max_sdk_version()) + "\n")
    file.write("target sdk version: " + str(a.get_target_sdk_version()) + "\n")
    file.close()


def certificate(a):  # CERTIFICATE
    file = open('certificate' + '.txt', 'w')
    for cert in a.get_certificates():
        file.write("the sha1 fingerprint: " + str(hashlib.sha1(cert.sha1).hexdigest()) + "\n")  # the sha1 fingerprint
        file.write("the sha256 fingerprint: " + str(hashlib.sha256(cert.sha256).hexdigest()) + "\n")  # the sha256 fingerprint
        file.write("issuer: " + cert.issuer.human_friendly + "\n")  # issuer
        file.write("subject, usually the same: " + cert.subject.human_friendly + "\n")  # subject, usually the same
        file.write("hash algorithm: " + cert.hash_algo + "\n")  # hash algorithm
        file.write("Signature algorithm: " + cert.signature_algo + "\n")  # Signature algorithm
        file.write("Serial number: " + str(cert.serial_number) + "\n")  # Serial number
    file.close()


def intent_filter(a):
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

    file = open('intents' + '.txt', 'w')
    for intent in intent_filters:
        file.write(intent + "\n")
    file.close()


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


def send_data_to_db():
    intent_filter(a)
    client = MongoClient('localhost', 27017)
    db = client['apps']
    series_collection = db['test_apps']
    post = {"id": 1,
            "activities": activities(a),
            "providers": providers(a),
            "services": services(a),
            "permissions": permission(a),
            "package_name": a.get_package(),
            "app_name": a.get_app_name(),
            "min_sdk": a.get_min_sdk_version(),
            "max_sdk": a.get_max_sdk_version(),
            "target_sdk": a.get_target_sdk_version(),
            "certificate": a.get_certificates(),
            "intent_filters": intent_filters,
            }

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print(post_id)


print("Input methods")
# search_methods(Methods.input, methodGenerationInput)
print("\n\n\n\n\n")
print("Output methods")
# search_methods(Methods.output, methodGenerationOutput)

# print(methodGenerationOutput)
# print(methodGenerationInput)
# print(Methods.output.keys())
# print(Methods.input.keys())
# print(dict(zip(Mapper.get_list_methods(Methods.output), methodGenerationOutput)))
send_data_to_db()
