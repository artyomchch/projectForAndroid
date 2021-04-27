from androguard import misc
from androguard import session

from androguard.misc import AnalyzeAPK
from androguard.session import Session
from androguard.core.bytecodes.apk import APK

from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.analysis.analysis import Analysis
from androguard.decompiler.decompiler import DecompilerJADX
from androguard.core.androconf import show_logging
import logging

from androguard.misc import AnalyzeAPK
import os
import time


def EXTRACT_METHOD_CALLS(a):
    app, list_of_dex, dx = AnalyzeAPK(a)
    for method in dx.get_methods():
        file.write("inside Method {} ".format(method.name) + ':' + '\n')
        #for _, call, _ in method.get_xref_to():
         #   file.write("    calling -> {} -- {}".format(call.class_name, call.name) + '\n')


begin = time.time()

for apk in os.listdir():
    file_name, file_extension = os.path.splitext(apk)
    file = open(file_name + '.txt', 'w')
    EXTRACT_METHOD_CALLS("Uber.apk")
    file.close()

end = time.time()

print(end - begin)
