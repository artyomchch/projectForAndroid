input = {
    "Landroidx/core/location/LocationManagerCompat;": ["getCurrentLocation"],
    "Landroid/location/LocationManager;": ["getCurrentLocation"],
    "Landroid/media/AudioRecord;": ["startRecording", "getAudioSessionId", "read"],
    "Landroid/media/MediaRecorder;": ["setAudioSource", "setOutputFormat", "setAudioEncoder", "prepare", "start", "stop"],
    "Landroid/hardware/SensorManager;": ["getDefaultSensor", "getDynamicSensorList"],
    "Landroid/hardware/Camera;": ["open", "takePicture", "getParameters", "getCameraInfo", "setParameters"],
    "Landroid/hardware/camera2/CameraManager;": ["openCamera", "getCameraIdList", "getCameraCharacteristics"],
    "Ljava/util/Calendar;": ["getInstance"],
    "Landroid/provider/VoicemailContract/Voicemails;": ["buildSourceUri"],
    "Landroid/provider/ContactsContract/Contacts;": ["getLookupUri", "lookupContact"],
    "Landroid/net/sip/SipManager;": ["getCallId", "getOfferSessionDescription", "getSessionFor", "makeAudioCall", "newInstance", "open"],
    "Landroid/telephony/SmsManager;": ["getDefault", "getSubscriptionId", "sendDataMessage", "sendMultimediaMessage", "sendMultipartTextMessage",
                                       "sendTextMessage", "sendTextMessageWithoutPersisting"],
    "Landroid/content/pm/PackageManager;": ["getInstallSourceInfo", "getInstalledApplications", "getInstalledModules", "getInstalledPackages",
                                            "getInstallerPackageName", "getApplicationInfo"],
    "Landroid/telephony/TelephonyManager;": ["getCallState", "getCallStateForSubscription", "getCellLocation", "getAllCellInfo",
                                             "getDeviceId", "getDeviceSoftwareVersion", "getImei", "getManufacturerCode", "getMeid", "getNetworkType",
                                             "getSimSerialNumber", "getSubscriberId", "getVoiceMailNumber"],
    "Landroid/accounts/AccountManager;": ["get", "getAccounts", "getAuthToken", "getPassword", "getPreviousName", "getUserData",
                                          "getAccountsAndVisibilityForPackage", "getAccountsByType", "getAccountsByTypeAndFeatures", "getAuthenticatorTypes",
                                          "getPackagesAndVisibilityForAccount"],
    "Lcom/android/billingclient/api/Purchase;": ["getAccountIdentifiers", "getDeveloperPayload", "getOrderId", "getOriginalJson", "getPackageName",
                                                 "getPurchaseState", "getPurchaseTime", "getPurchaseToken", "getQuantity", "getSkus", "getSignature"],
    "Landroid/hardware/fingerprint/FingerprintManager;": ["authenticate"],
    "Landroid/hardware/biometrics/BiometricPrompt;": ["authenticate", "getAllowedAuthenticators", "getDescription", "getNegativeButtonText", "getSubtitle",
                                                      "getTitle"],
    "Landroid/net/wifi/WifiManager;": ["getConfiguredNetworks", "getConnectionInfo", "getDhcpInfo", "getPasspointConfigurations", "getScanResults",
                                       "getWifiState", "getNetworkSuggestions", "getPasspointConfigurations"],
    "Landroid/net/ConnectivityManager;": ["getActiveNetwork", "getActiveNetworkInfo", "getAllNetworkInfo", "getBoundNetworkForProcess", "getConnectionOwnerUid",
                                          "getDefaultProxy", "getLinkProperties", "getMultipathPreference", "getNetworkCapabilities",
                                          "getNetworkInfo", "getNetworkWatchlistConfigHash", "getProcessDefaultNetwork"],
    "Landroid/net/NetworkInfo;": ["describeContents", "getDetailedState", "getExtraInfo", "getState", "getSubtype", "getSubtypeName", "getType", "getTypeName"],
    "Landroid/net/NetworkCapabilities;": ["getCapabilities", "describeContents", "getNetworkSpecifier", "getOwnerUid", "getSignalStrength", "getTransportInfo"],
    "Landroid.os.Environment;": ["getDataDirectory", "getExternalStorageDirectory", "getExternalStorageState", "getStorageState", "getDownloadCacheDirectory"]
}

output = {
    "Ljava/net/URL;": ["openStream", "getContent", "getHost", "getFile", "getPort", "getProtocol", "getRef", "hashCode", "equals",
                       "toExternalForm", "toString", "openConnection"],
    "Ljava/net/Socket;": ["bind", "connect", "close", "getChannel", "getInetAddress", "getLocalPort", "getLocal", "socketAddress",
                          "getReceive", "isClosed", "setReceive"],
    "Landroid/net/Uri;": ["buildUpon", "compareTo", "decode", "encode", "equals", "fromParts", "getAuthority", "getEncodedQuery", "getHost",
                          "getLastPathSegment", "getPath", "getPathSegments", "getPort", "getQuery", "getScheme", "specificPart", "normalizeScheme", "parse",
                          "writeToParcel"],
    "Landroid/net/Network;": ["bindSocket", "describeContents", "fromNetworkHandle", "getAllByName", "getByName", "getNetworkHandle", "getSocketFactory",
                              "hashCode", "openConnection",
                              "toString", "writeToParcel"],
    "Lorg/apache/http/HttpRequest;": ["getAuthority", "getMethod", "getPath", "getRequestUri", "getScheme", "getUri", "setAuthority", "setPath", "setScheme",
                                      "setUri"],
    "Lorg/apache/http/HttpResponse;": ["getEntity", "getLocale", "getStatusLine", "setEntity", "setLocale", "setReasonPhrase", "setStatusCode",
                                       "setStatusLine"],
    "Lretrofit2/Retrofit$Builder;": ["baseUrl", "addCallAdapter"],
    "Lretrofit2/RequestFactory$Builder;": ["build"],
    "Lokhttp3/OkHttpClient$Builder;": ["authenticator", "cache", "callTimeoutMillis", "certificatePinner", "connectionPool", "dispatcher", "dns",
                                       "interceptors",
                                       "newBuilder", "newCall", "newWebSocket", "protocols", "proxy", "authenticator", "proxySelector", "readTimeoutMillis",
                                       "socketFactory", "writeTimeoutMillis"]
}
