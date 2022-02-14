import argparse
import hashlib
import os

from androguard import misc
from pymongo import MongoClient
from termcolor import cprint

parser = argparse.ArgumentParser()

parser.add_argument("path")

args = parser.parse_args()

input_classes = {
    "Landroidx/core/location/LocationManagerCompat;": ["getCurrentLocation"],
    "Landroid/location/LocationManager;": ["getCurrentLocation", "getLastKnownLocation", "requestLocationUpdates", "requestSingleUpdate"],
    "Lcom/google/android/gms/location/FusedLocationProviderClient;": ["getCurrentLocation", "getLastLocation", "requestLocationUpdates"],  # Question????
    "Landroid/media/AudioRecord;": ["startRecording", "getAudioSessionId", "read"],
    "Landroid/media/MediaRecorder;": ["prepare", "start", "stop"],
    "Landroid/hardware/SensorManager;": ["getDefaultSensor", "getDynamicSensorList"],
    "Landroid/hardware/Camera;": ["open", "takePicture", "startPreview"],
    "Landroid/hardware/camera2/CameraManager;": ["openCamera"],
    "Landroid/hardware/camera2/CameraCaptureSession;": ["capture"],
    "Landroid/hardware/camera2/CameraDevice;": ["createCaptureRequest"],
    "Landroidx/camera/core/ImageCapture;": ["takePicture"],
    "Landroidx/camera/video/PendingRecording;": ["start"],
    "Ljava/util/Calendar;": ["getInstance"],
    "Landroid/provider/VoicemailContract/Voicemails;": ["buildSourceUri"],
    "Landroid/provider/ContactsContract/Contacts;": ["getLookupUri", "lookupContact"],  # + constants
    "Landroid/provider/Telephony/Sms;": [],  # + constants / fields
    "Landroid/net/sip/SipManager;": ["getCallId", "getOfferSessionDescription", "getSessionFor", "makeAudioCall", "newInstance", "open"],
    "Landroid/telephony/TelephonyManager;": ["getCardIdForDefaultEuicc", "getLine1Number", "getCellLocation", "getAllCellInfo", "getDeviceId",
                                             "getDeviceSoftwareVersion", "getImei", "getManufacturerCode",
                                             "getMeid", "getSimSerialNumber", "getSubscriberId", "getVoiceMailNumber"],
    "Landroidx/core/telephony/TelephonyManagerCompat;": ["getImei", "getSubscriberId"],
    "Landroid/os/Environment;": ["getRootDirectory", "getExternalStoragePublicDirectory", "getStorageDirectory", "getDataDirectory",
                                 "getExternalStorageDirectory", "getDownloadCacheDirectory", "getExternalStoragePublicDirectory"],
    "Landroid/accounts/AccountManager;": ["get", "getAccounts", "getAuthToken", "getAuthTokenByFeatures", "getPassword", "getPreviousName", "getUserData",
                                          "getAccountsAndVisibilityForPackage", "getAccountsByType", "getAccountsByTypeAndFeatures", "getAuthenticatorTypes",
                                          "getPackagesAndVisibilityForAccount"],
    "Lcom/android/billingclient/api/Purchase;": ["getAccountIdentifiers", "getDeveloperPayload", "getOrderId", "getOriginalJson", "getPackageName",
                                                 "getPurchaseState", "getPurchaseTime", "getPurchaseToken", "getQuantity", "getSkus", "getSignature"],
    "Lcom/android/billingclient/api/PurchaseHistoryRecord;": ["getOriginalJson", "getDeveloperPayload"],
    "Landroid/hardware/fingerprint/FingerprintManager;": ["authenticate"],
    "Landroidx/core/hardware/fingerprint/FingerprintManagerCompat;": ["authenticate"],
    "Landroid/hardware/biometrics/BiometricPrompt;": ["authenticate", "getAllowedAuthenticators", "getDescription", "getNegativeButtonText", "getSubtitle",
                                                      "getTitle"],
    "Landroid/net/wifi/WifiManager;": ["getCallerConfiguredNetworks", "getNetworkSuggestions", "getConfiguredNetworks", "getConnectionInfo", "getDhcpInfo",
                                       "getPasspointConfigurations", "getScanResults", "getNetworkSuggestions", "registerScanResultsCallback"],
    "Landroid/net/ConnectivityManager;": ["getActiveNetwork", "getActiveNetworkInfo", "getAllNetworkInfo", "getBoundNetworkForProcess", "getConnectionOwnerUid",
                                          "getDefaultProxy", "getLinkProperties", "getMultipathPreference", "getNetworkCapabilities",
                                          "getNetworkInfo", "getNetworkWatchlistConfigHash", "getProcessDefaultNetwork", "registerNetworkCallback"],
    "Landroid/net/NetworkInfo;": ["getDetailedState"],
    "Landroid/net/NetworkCapabilities;": ["getOwnerUid", "getSignalStrength", "getTransportInfo"],
    "Landroidx/core/net/ConnectivityManagerCompat;": ["getNetworkInfoFromBroadcast"],
    "Lcom/google/android/things/bluetooth/BluetoothConfigManager;": ["getBluetoothClass", "getInstance"],
}

input_constants = {
    "CallLog/Calls": ["CONTENT_URI", "CACHED_LOOKUP_URI", "CACHED_MATCHED_NUMBER", "CACHED_NAME", "CACHED_PHOTO_URI", "COUNTRY_ISO", "DATA_USAGE", "DATE",
                      "DURATION", "FEATURES", "GEOCODED_LOCATION", "INCOMING_TYPE", "LOCATION", "NUMBER", "OUTGOING_TYPE", "PHONE_ACCOUNT_COMPONENT_NAME",
                      "PHONE_ACCOUNT_ID", "TYPE", "VIA_NUMBER", "VOICEMAIL_TYPE", "VOICEMAIL_URI"],
    "Contacts": ["vnd.android.cursor.item/name", "vnd.android.cursor.item/contact", "vnd.android.cursor.item/email_v2",
                 "vnd.android.cursor.item/websitevnd.android.cursor.item/note", "vnd.android.cursor.item/contact_eventdata6",
                 "vnd.android.cursor.item/postal-address_v2data7data8data9data10", "vnd.android.cursor.item",
                 "vnd.android.cursor.item/im", "vnd.android.cursor.item/organization", "vnd.android.cursor.item/group_membership",
                 "vnd.android.cursor.item/phone_v", "vnd.android.cursor.dir/name", "vnd.android.cursor.dir/contact", "vnd.android.cursor.dir/email_v2",
                 "vnd.android.cursor.dir/websitevnd.android.cursor.dir/note", "vnd.android.cursor.dir/contact_eventdata6",
                 "vnd.android.cursor.dir/postal-address_v2data7data8data9data10", "vnd.android.cursor.dir",
                 "vnd.android.cursor.dir/im", "vnd.android.cursor.dir/organization", "vnd.android.cursor.dir/group_membership",
                 "vnd.android.cursor.dir/phone_v"],
    "Calls": ["vnd.android.cursor.item/calls", "vnd.android.cursor.dir/calls"],
    "SMS": ["content://sms/inbox", "content://sms/sent", "content://sms/draft"],
    "Profile": ["vnd.android.cursor.item/vnd.org.telegram.messenger.android.profileTelegram", "vnd.android.cursor.item/vnd.com.whatsapp.profile",
                "vnd.android.cursor.item/vnd.com.viber.voip.viber_number_message", "vnd.android.cursor.item/vnd.org.thoughtcrime.securesms",
                "vnd.android.cursor.item/vnd.facebook.profile", "vnd.android.cursor.item/vnd.googleplus.profile",
                "vnd.android.cursor.item/vnd.com.linkedin.android.profile"]

}

output = {
    "Ljava/net/URL;": ["openStream", "getHost", "getContent", "getFile", "getPort", "getProtocol", "getRef", "hashCode", "toString", "openConnection"],
    "Ljava/net/Socket;": ["bind", "connect", "getChannel", "getInetAddress", "getLocalPort", "getLocal", "socketAddress",
                          "getReceive", "setReceive"],
    "Ljava/net/URLConnection;": ["connect", "getContent", "getContentEncoding", "getContentType", "getDate", "getDefaultAllowUserInteraction",
                                 "getDefaultRequestProperty", "getDefaultUseCaches", "getDoInput", "getDoOutput", "getHeaderField", "getInputStream", "getURL",
                                 "setDoInput", "setDoOutput", "setRequestProperty", "setUseCaches", "setIfModifiedSince"],
    "Lorg/apache/http/conn/HttpRequest;": ["getAuthority", "getMethod", "getPath", "getRequestUri", "getScheme", "getUri", "setAuthority", "setPath",
                                           "setScheme", "setUri"],
    "Lorg/apache/http/conn/HttpResponse;": ["getEntity", "getLocale", "getStatusLine", "setEntity", "setLocale", "setReasonPhrase", "setStatusCode",
                                            "setStatusLine"],
    "Landroid/net/Uri;": ["buildUpon", "decode", "encode", "fromParts", "getAuthority", "getEncodedQuery", "getHost",
                          "getLastPathSegment", "getPath", "getPathSegments", "getPort", "getQuery", "getScheme", "specificPart", "parse", "writeToParcel"],
    "Landroid/net/LocalServerSocket;": ["accept", "getLocalSocketAddress"],
    "Landroid/net/LocalSocket;": ["bind", "connect"],
    "Landroid/net/Network;": ["bindSocket", "describeContents", "fromNetworkHandle", "getAllByName", "getByName", "getNetworkHandle", "getSocketFactory",
                              "openConnection", "writeToParcel"],
    "Lretrofit2/Retrofit$Builder;": ["baseUrl", "addCallAdapter"],
    "Lretrofit2/RequestFactory$Builder;": ["build", "callbackExecutor", "client"],
    "Lokhttp3/OkHttpClient$Builder;": ["authenticator", "cache", "callTimeoutMillis", "certificatePinner", "connectionPool", "dispatcher", "dns",
                                       "interceptors", "newBuilder", "newCall", "newWebSocket", "protocols", "proxy", "proxySelector",
                                       "readTimeoutMillis", "socketFactory", "writeTimeoutMillis"],
    "Lokhttp4/OkHttpClient$Builder;": ["authenticator", "cache", "callTimeoutMillis", "certificatePinner", "connectionPool", "dispatcher", "dns",
                                       "interceptors", "newBuilder", "newCall", "newWebSocket"],
    "Lokhttp2/OkHttpClient$Builder;": ["open"],
    "Lcom/android/volley/toolbox/Volley;": ["newRequestQueue"],
    "Lcom/android/volley/RequestQueue;": ["add"],
    "Lcom/koushikdutta/ion/builder/LoadBuilder;": ["load"],
    "Lcom/google/firebase/FirebaseDatabase;": ["getApp", "getInstance", "getReference", "getReferenceFromUrl", "goOffline", "goOnline"],
    "Lcom/google/firebase/FirebaseAuth;": ["getInstance", "createUserWithEmailAndPassword", "signInWithEmailAndPassword", "signInWithCredential",
                                           "signInAnonymously", "signInWithCustomToken", "getCurrentUser"],
    "Lcom/google/firebase/FirebaseApp;": ["getApps", "getInstance", "getName", "getOptions", "initializeApp"],
    "Lcom/google/firebase/FirebaseStorage;": ["getApp", "getInstance", "getMaxDownloadRetryTimeMillis", "getMaxOperationRetryTimeMillis",
                                              "getMaxUploadRetryTimeMillis", "getReference", "getReferenceFromUrl"],
    "Landroid/telephony/SmsManager;": ["sendDataMessage", "sendMultimediaMessage", "sendMultipartTextMessage", "sendTextMessage"],
    "Landroid/net/sip/SipManager;": ["makeAudioCall", "open"],
}


def hash_id_app(apk_file):
    with open(apk_file, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def activities(a): return a.get_activities()  # ACTIVITIES


def providers(a): return a.get_providers()  # PROVIDERS


def services(a): return a.get_services()  # SERVICES


def permission(a): return a.get_permissions()  # PERMISSIONS


def certificate(a):  # CERTIFICATE
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


def intent_filter(a):
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


def search_methods(type_methods, method_generation, found_methods, dx):
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


def search_constants(dx):
    constant_methods = {}
    constants = []
    find_constants = []
    generation_code = []

    for const in input_constants.values():
        constants.extend(const)

    for item in dx.get_strings_analysis():
        for con in constants:
            if con.lower() == item:
                find_constants.append(item)

    print(find_constants)

    for classes in input_constants:
        constants = []

        for const in input_constants[classes]:
            check = False
            for i in find_constants:
                if i == const.lower():
                    constants.append(const)
                    generation_code.append(1)
                    check = True
            if check is not True:
                generation_code.append(0)
            if len(constants) != 0:
                constant_methods.update({classes: constants})
    print(generation_code)
    print(len(generation_code))
    return constant_methods, generation_code


def mapper_data_methods(dx):
    method_generation_input = []
    method_generation_output = []
    found_methods_input = {}
    found_methods_output = {}
    data_methods = {}
    search_methods(input_classes, method_generation_input, found_methods_input, dx)
    data_methods["found_input_methods"] = found_methods_input
    data_methods["input_methods_generation"] = method_generation_input
    search_methods(output, method_generation_output, found_methods_output, dx)
    data_methods["found_output_methods"] = found_methods_output
    data_methods["output_methods_generation"] = method_generation_output
    methods, code = search_constants(dx)
    found_methods_input.update(methods)
    method_generation_input.extend(code)

    return data_methods


def send_data_to_db(category, apk_file):
    a, d, dx = misc.AnalyzeAPK(apk_file)
    intent_filter(a)
    client = MongoClient('localhost', 27017)
    db = client['apps']
    post = {"id": hash_id_app(apk_file),
            "activities": activities(a),
            "providers": providers(a),
            "services": services(a),
            "permissions": permission(a),
            "package_name": a.get_package(),
            "app_name": a.get_app_name(),
            "min_sdk": a.get_min_sdk_version(),
            "max_sdk": a.get_max_sdk_version(),
            "target_sdk": a.get_target_sdk_version(),
            "certificate": certificate(a),
            "intent_filters": intent_filter(a),
            "methods": mapper_data_methods(dx),
            "category": category,
            }

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print(post_id)


def main_execute_app(path):
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            print(directory)
            for (_, _, file) in os.walk(path + directory):
                for file_apk in file:
                    if '.apk' in file_apk:
                        send_data_to_db(directory, path +
                                        "/" + directory + "/" + file_apk)
                        print(file_apk)


main_execute_app(args.path)
