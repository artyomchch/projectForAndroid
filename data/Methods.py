input = {
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
                                       "interceptors", "newBuilder", "newCall", "newWebSocket", "protocols", "proxy", "authenticator", "proxySelector",
                                       "readTimeoutMillis", "socketFactory", "writeTimeoutMillis"],
    "Lokhttp4/OkHttpClient$Builder;": ["authenticator", "cache", "callTimeoutMillis", "certificatePinner", "connectionPool", "dispatcher", "dns",
                                       "interceptors", "newBuilder", "newCall", "newWebSocket"],
    "Lokhttp2/OkHttpClient$Builder;": ["open"],
    "Lcom/android/voley/Volley;": ["newRequestQueue"],
    "Lcom/android/voley/RequestQueue;": ["add"],
    "Lcom/kouhikdutta/ion/ION;": ["load"],
    "Lcom/google/firebase/FirebaseDatabase;": ["getApp", "getInstance", "getReference", "getReferenceFromUrl", "goOffline", "goOnline"],
    "Lcom/google/firebase/FirebaseAuth;": ["getInstance", "createUserWithEmailAndPassword", "signInWithEmailAndPassword", "signInWithCredential",
                                           "signInAnonymously", "signInWithCustomToken", "getCurrentUser"],
    "Lcom/google/firebase/FirebaseApp;": ["getApps", "getInstance", "getName", "getOptions", "initializeApp"],
    "Lcom/google/firebase/FirebaseStorage;": ["getApp", "getInstance", "getMaxDownloadRetryTimeMillis", "getMaxOperationRetryTimeMillis",
                                              "getMaxUploadRetryTimeMillis", "getReference", "getReferenceFromUrl"],
    "Landroid/telephony/SmsManager;": ["sendDataMessage", "sendMultimediaMessage", "sendMultipartTextMessage", "sendTextMessage"],
    "Landroid/net/sip/SipManager;": ["makeAudioCall", "open"],
}
