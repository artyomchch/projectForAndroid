import hashlib

from androguard import misc
from pymongo import MongoClient
from termcolor import cprint

from data import Methods

a, d, dx = misc.AnalyzeAPK("../apk/test_apk.apk")


def hash_id_app():
    with open("../apk/test_apk.apk", "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def activities(): return a.get_activities()  # ACTIVITIES


def providers(): return a.get_providers()  # PROVIDERS


def services(): return a.get_services()  # SERVICES


def permission(): return a.get_permissions()  # PERMISSIONS


def certificate():  # CERTIFICATE
    certificate_list = {}
    for cert in a.get_certificates():
        certificate_list["sha1"] = hashlib.sha1(cert.sha1).hexdigest()
        certificate_list["sha256"] = hashlib.sha256(cert.sha256).hexdigest()
        certificate_list["issuer_human_friendly"] = cert.issuer.human_friendly
        certificate_list["subject_human_friendly"] = cert.subject.human_friendly
        certificate_list["hash_algo"] = cert.hash_algo
        certificate_list["signature_algo"] = cert.signature_algo
        certificate_list["serial_number"] = cert.serial_number
    return certificate_list


def intent_filter():
    intent_filters = {}
    activity = a.get_activities()
    receivers = a.get_receivers()
    service = a.get_services()

    if activity is not None:
        for i in activity:
            filters = a.get_intent_filters("activity", i)
            if filters is not None and len(filters) > 0:
                intent_filters[i] = filters

    if receivers is not None:
        for i in receivers:
            filters = a.get_intent_filters("receiver", i)
            if filters is not None and len(filters) > 0:
                intent_filters[i] = filters

    if service is not None:
        for i in service:
            filters = a.get_intent_filters("service", i)
            if filters is not None and len(filters) > 0:
                intent_filters[i] = filters

    return intent_filters


def search_methods(type_methods, method_generation, found_methods):
    for i in type_methods:
        print("Use Class: ", i)
        try:
            use_class = False
            for meth in dx.classes[i].get_methods():
                methods_classes = []
                for _, call, _ in meth.get_xref_to():
                    for methods in type_methods[i]:
                        if methods == call.name:
                            use_class = True
                            cprint("found method: --> {}".format(call.name), "green")
                            methods_classes.append(call.name)
                            found_methods[i] = methods_classes
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


def mapper_data_methods():
    method_generation_input = []
    method_generation_output = []
    found_methods_input = {}
    found_methods_output = {}
    data_methods = {}
    search_methods(Methods.input, method_generation_input, found_methods_input)
    data_methods["found_input_methods"] = found_methods_input
    data_methods["input_methods_generation"] = method_generation_input
    search_methods(Methods.output, method_generation_output, found_methods_output)
    data_methods["found_output_methods"] = found_methods_output
    data_methods["output_methods_generation"] = method_generation_output

    return data_methods


def send_data_to_db(category):
    intent_filter()
    client = MongoClient('localhost', 27017)
    db = client['apps']
    post = {"id": hash_id_app(),
            "activities": activities(),
            "providers": providers(),
            "services": services(),
            "permissions": permission(),
            "package_name": a.get_package(),
            "app_name": a.get_app_name(),
            "min_sdk": a.get_min_sdk_version(),
            "max_sdk": a.get_max_sdk_version(),
            "target_sdk": a.get_target_sdk_version(),
            "certificate": certificate(),
            "intent_filters": intent_filter(),
            "methods": mapper_data_methods(),
            "category": category,
            }

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print(post_id)


send_data_to_db("TEST_CATEGORY")
