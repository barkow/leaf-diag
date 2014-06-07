import socket
import sys
import struct
import array
import pprint
import binascii

class dtcAndStatusRecord(dict):
    def __init__(self, dtc, status, description):
        self["dtc"] = dtc
        self["status"] = status
        self["description"] = description  

class UDSResponse(object):
    def __init__(self):
        self.serviceId = None
        self.negativeResponseServiceId = None
        self.responseCode = None
        self.data = None
        pass
    
    def isNegativeReponse(self):
        return self.negativeResponseServiceId is not None
    
    def deserialize(self, raw):
        #Prüfen ob negative response vorliegt
        if raw[0] == 0x7f:
            self.negativeResponseServiceId = 0x7f
            self.serviceId = raw[1]
            self.responseCode = raw[2]
            return
        #Da keine UUDT Responses unterstützt werden, liegt im ersten Byte der SID
        self.serviceId = raw[0]
        self.data = raw[1:]
        
class UDSRequest(object):
    def __init__(self):
        self.serviceId = None
        self.subFunction = None
        self.data = None
        
    def serialize(self):
        if self.subFunction is None:
            return array.array('B', [self.serviceId]) + self.data
        else:
            return array.array('B', [self.serviceId, self.subFunction]) + self.data
        
    def getResponse(self, rawResponse):
        return None            

class startDiagnosticSessionResponse(UDSResponse):    
    def __init__(self):
        super().__init__()
        self.sessionId = None
        
    def deserialize(self, raw):
        super().deserialize(raw)   
        self.sessionId = self.data[0]     

class startDiagnosticSessionRequest(UDSRequest):
    def __init__(self, sessionId):
        super().__init__()
        self.serviceId = 0x10
        self.data = array.array('B', [sessionId])
    
    def getResponse(self, rawResponse):
        res = startDiagnosticSessionResponse()
        res.deserialize(rawResponse)
        return (res)

class readDtcInformationByStatusMaskResponse(UDSResponse):
    def __init__(self):
        super().__init__()
        self.statusMask = None
        self.dtcAndStatusRecords = []
        
    def deserialize(self, raw):
        super().deserialize(raw)   
        self.statusMask = self.data[1]
        k = len(self.data[2:])
        i = 0
        while i*4 < k:
            dtcAndStatus = self.data[(2+(i*4)):(2+(i*4)+4)]
            record = dtcAndStatusRecord(dtcAndStatus[0] * 256 * 256 + dtcAndStatus[1] * 256 + dtcAndStatus[2], dtcAndStatus[3], "")
            self.dtcAndStatusRecords.append(record)
            i += 1

class readDtcInformationByStatusMaskRequest(UDSRequest):
    def __init__(self, statusMask):
        super().__init__()
        self.serviceId = 0x19
        self.data = array.array('B', [0x02, statusMask])
    
    def getResponse(self, rawResponse):
        res = readDtcInformationByStatusMaskResponse()
        res.deserialize(rawResponse)
        return (res)

class clearDiagnosticInformationResponse(UDSResponse):    
    def __init__(self):
        super().__init__()
        
    def deserialize(self, raw):
        super().deserialize(raw)   

class clearDiagnosticInformationRequest(UDSRequest):
    def __init__(self, groupOfDtc):
        super().__init__()
        self.serviceId = 0x14
        self.data = array.array('B', groupOfDtc)
    
    def getResponse(self, rawResponse):
        res = clearDiagnosticInformationResponse()
        res.deserialize(rawResponse)
        return (res)


class UDSEcu(object):
        
    def __build_can_frame(self, can_id, data):
        can_frame_fmt = "=IB3x8s"
        can_dlc = len(data)
        
        # data = data.ljust(8, b'\x00')
        return struct.pack(can_frame_fmt, can_id, can_dlc, data)
    
    def __init__(self, interface, rxId, txId):
        self.__s = socket.socket(socket.AF_CAN, socket.SOCK_DGRAM, socket.CAN_ISOTP)
        # Timeout für ausbleibende Responses auf 5s setzen
        self.__s.settimeout(5.0)
        self.__s.bind((interface, txId, rxId))
        return
    
    def __del__(self):
        self.__s.close()
        
    def __sendRequest(self, request):
        self.__s.send(request.serialize())
        try:
            data = self.__s.recv(4096)
        except socket.timeout:
            return None
        
        return request.getResponse(data)
    
    def getStoredErrors(self):
        # Diagnose Session starten
        req = startDiagnosticSessionRequest(0xC0)
        res = self.__sendRequest(req)
        
        if res is None:
            return False
        
        if res.isNegativeReponse():
            return False
        
        # DTCs auslesen
        req = readDtcInformationByStatusMaskRequest(0xff)
        res = self.__sendRequest(req);
        
        if res is None:
            return False
        
        if res.isNegativeReponse():
            return False

        return res.dtcAndStatusRecords
    
    def clearStoredErrors(self):
        # Diagnose Session starten
        req = startDiagnosticSessionRequest(0xC0)
        res = self.__sendRequest(req)
        
        if res is None:
            return False
        
        if res.isNegativeReponse():
            return False
        
        # Fehlerspeicher löschen
        req = clearDiagnosticInformationRequest([0xff, 0xff, 0xff])
        res = self.__sendRequest(req);
        
        if res is None:
            return False
        
        return not res.isNegativeReponse()
