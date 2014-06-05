import http.server
import socketserver
import pprint
import json
import UDSEcu
import os

PORT = 80

class MyHandler(http.server.BaseHTTPRequestHandler):
    ecus = dict()
    
    def renderHtml(self, request):
        if request == "/":
            filename = "index.html"
        else:
            filename = request[1:]
        
        self.send_response(200)
        if os.path.splitext(filename)[1] == ".js":
            self.send_header("Content-type", "application/javascript")
        if os.path.splitext(filename)[1] == ".css":
            self.send_header("Content-type", "text/css")
        if os.path.splitext(filename)[1] == ".html":
            self.send_header("Content-type", "text/html")
                    
        
        
        self.end_headers()
        
        
        if os.path.isfile(filename):
            f = open(filename, "r")
            self.wfile.write(f.read().encode("utf-8"))
            f.close()
    
    def renderJson(self, obj):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode("utf-8"))
        return
    
    def renderError(self, status, message):
        self.send_error(status, message)
        return
    
    def doClearErrorMemory(self, ecuId):
        if ecuId not in self.ecus:
            self.renderError(404, "Ecu not found")
            return
        
        myEcu = UDSEcu.UDSEcu(self.ecus[ecuId]["rxId"], self.ecus[ecuId]["txId"])
        success = myEcu.clearStoredErrors()
        if success:
            self.renderJson(True)
            return
        else:
           self.renderError(500, "Error Memory cleraing failed") 
    
    def doShowEcuInfo(self, ecuId):
        if ecuId not in self.ecus:
            self.renderError(404, "Ecu not found")
            return
        self.renderJson(self.ecus[ecuId])
        return
    
    def doReadErrorMemory(self, ecuId):
        if ecuId not in self.ecus:
            self.renderError(404, "Ecu not found")
            return
        
        myEcu = UDSEcu.UDSEcu(self.ecus[ecuId]["rxId"], self.ecus[ecuId]["txId"])
        errors = myEcu.getStoredErrors()
        del myEcu
        if errors == False:
            self.renderError(500, "Ecu not responding or negative response received")
            return
        
        # Bezeichnung für DTCs eintragen, wenn bekannt
        for error in errors:
            if error["dtc"] in self.ecus[ecuId]["knownDtcs"]:
                error["description"] = self.ecus[ecuId]["knownDtcs"][error["dtc"]]
            else:
                error["description"] = "n.a."
        
        self.renderJson(errors)
        return
    
    def parseEcusRequest(self, request, requestType):
        resourceRequest = request.split('/', 2)
        ecuId = resourceRequest[0]
        if ecuId == "":
            self.renderError(400, "Ecu ID missing")
            print("ecuId fehlt")
            return
        
        if (requestType == "GET") and ((len(resourceRequest) < 2) or (resourceRequest[1] == "")):
            self.doShowEcuInfo(ecuId)
            return
        
        if (requestType == "GET") and (resourceRequest[1] == "errormemory"):
            self.doReadErrorMemory(ecuId)
            return
        
        if (requestType == "DELETE") and (resourceRequest[1] == "errormemory"):
            print("clear " + ecuId)
            self.doClearErrorMemory(ecuId)
            return
        
        self.renderError(400, "Unknown request")
        return
        
    def parseRequest(self, request, requestType):
        resourceRequest = request.split("/", 2)
        if resourceRequest[1] == "ecus":
            self.parseEcusRequest(resourceRequest[2], requestType)
            return
        
        #Sonst Website ausliefern
        self.renderHtml(request)
        
        
    def do_GET(self):        
        self.parseRequest(self.path, "GET")
        return
    
    def do_DELETE(self):        
        self.parseRequest(self.path, "DELETE")
        return


ecus = {
    "ecu1" : {
        "name" : "Ecu 1", 
        "txId" : 0x700, 
        "rxId" : 0x600,
        "knownDtcs" : {0x112233: "Schütze kleben geblieben"}
    },
    "ecu2" : {
        "name" : "Ecu 2", 
        "txId" : 0x701, 
        "rxId" : 0x601,
        "knownDtcs" : {}
    }
}

# Handler = http.server.SimpleHTTPRequestHandler
Handler = MyHandler
Handler.ecus = ecus
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
