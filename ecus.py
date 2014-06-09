ecus = {
    "ecu1" : {
        "name" : "Ecu 1", 
        "txId" : 0x70e, 
        "rxId" : 0x70f,
        "knownDtcs" : {0x112233: "Schütze kleben geblieben"}
    },
    "ecu2" : { # ReadDTC -> 0x11 (unknown )
        "name" : "Ecu 2", 
        "txId" : 0x71d, 
        "rxId" : 0x72d,
        "knownDtcs" : {}
    },
    "ecu3" : { # StartDiagnostic Session -> 0x22 (Conditions not correct)
        "name" : "Ecu 3", 
        "txId" : 0x71e, 
        "rxId" : 0x72e,
        "knownDtcs" : {}
    },
    "ecu4" : {
        "name" : "Ecu 4", 
        "txId" : 0x73f, 
        "rxId" : 0x761,
        "knownDtcs" : {}
    },
    "ecu5" : { # Clear Error Memory -> 0x23 (unknown)
        "name" : "Ecu 5", 
        "txId" : 0x740, 
        "rxId" : 0x760,
        "knownDtcs" : {}
    },
    "ecu6" : {
        "name" : "Ecu 6", 
        "txId" : 0x742, 
        "rxId" : 0x762,
        "knownDtcs" : {}
    },
    "ecu7" : {
        "name" : "Ecu 7", 
        "txId" : 0x743, 
        "rxId" : 0x763,
        "knownDtcs" : {}
    },
    "ecu8" : {
        "name" : "Ecu 8", 
        "txId" : 0x744, 
        "rxId" : 0x764,
        "knownDtcs" : {}
    },
    "ecu9" : {
        "name" : "Ecu 9", 
        "txId" : 0x745, 
        "rxId" : 0x765,
        "knownDtcs" : {}
    },
    "ecu10" : {
        "name" : "Ecu 10", 
        "txId" : 0x74d, 
        "rxId" : 0x76d,
        "knownDtcs" : {}
    },
    "ecu11" : {
        "name" : "Ecu 11", 
        "txId" : 0x752, 
        "rxId" : 0x772,
        "knownDtcs" : {}
    },
    "ecu12" : {
        "name" : "Ecu 12", 
        "txId" : 0x784, 
        "rxId" : 0x78c,
        "knownDtcs" : {}
    },
    "ecu13" : {
        "name" : "Ecu 13", 
        "txId" : 0x792, 
        "rxId" : 0x793,
        "knownDtcs" : {}
    },
    "ecu14" : {
        "name" : "Ecu 14", 
        "txId" : 0x797, 
        "rxId" : 0x79a,
        "knownDtcs" : {}
    },
    "ecu15" : {
        "name" : "Ecu 15", 
        "txId" : 0x79b, 
        "rxId" : 0x7bb,
        "knownDtcs" : {}
    },
    "ecu16" : {
        "name" : "Ecu 16", 
        "txId" : 0x79d, 
        "rxId" : 0x7bd,
        "knownDtcs" : {}
    },
    "ecu17" : { # Start Diagnostic Session -> 0x12 (Sub Function not supported)
        "name" : "Ecu 17", 
        "txId" : 0x7f1, 
        "rxId" : 0x7f9,
        "knownDtcs" : {}
    }
}
