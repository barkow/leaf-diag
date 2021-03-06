function EcuViewModel(id){
  var self = this;
  self.id = id;
  self.name = ko.observable();
  self.canClearErrorMemory = ko.observable(false);
  self.storedDtcs = ko.observableArray();
  self.numberOfStoredDtcs = ko.observable(0);
  self.commFailure = ko.observable(false);
  self.requestActive = ko.observable(false);
  
  self.readErrorMemory = function(){
    console.log("Read Error Memory of " + self.name());
    self.requestActive(true);
    $.get("ecus/"+self.id+"/errormemory", function(data) {
      self.storedDtcs.removeAll();
      console.log(data)
      $.each($.parseJSON(data), function(index, element){
        self.storedDtcs.push(element);
      });
      self.numberOfStoredDtcs($.parseJSON(data).length);
      self.canClearErrorMemory((self.numberOfStoredDtcs() > 0));
      self.commFailure(false);
    })
    .fail(function(){
      self.commFailure(true);
    })
    .always(function(){
      self.requestActive(false);
    });
    
  };
  
  self.clearErrorMemory = function(){
    console.log("Clear Error Memory of " + self.name());
    self.requestActive(true);
    $.ajax({
      url: "ecus/"+self.id+"/errormemory", 
      type: "DELETE"
    })    
    .done(function(data){
      self.commFailure(false);
    })
    .fail(function(){
      self.commFailure(true);
    })
    .always(function(){
      self.requestActive(false);
    });
    self.readErrorMemory();
  };

  //Init Model
  $.get("ecus/"+self.id, function(data) {
    console.log(data)
    self.name($.parseJSON(data).name);
    self.commFailure(false);
  });
}

function LeafViewModel() {
    var self = this;    
    
    //Submodels
    self.ecus = ko.observableArray([
      new EcuViewModel("ecu1"), 
      new EcuViewModel("ecu2"),
      new EcuViewModel("ecu3"),
      new EcuViewModel("ecu4"),
      new EcuViewModel("ecu5"),
      new EcuViewModel("ecu6"),
      new EcuViewModel("ecu7"),
      new EcuViewModel("ecu8"),
      new EcuViewModel("ecu9"),
      new EcuViewModel("ecu10"),
      new EcuViewModel("ecu11"),
      new EcuViewModel("ecu12"),
      new EcuViewModel("ecu13"),
      new EcuViewModel("ecu14"),
      new EcuViewModel("ecu15"),
      new EcuViewModel("ecu16"),
      new EcuViewModel("ecu17")
    ]);
    
    // Data
    self.pages = ['Home'];
    self.chosenPageId = ko.observable();
    self.totalNumberOfStoredDtcs = ko.computed(function(){
      var no = 0;
      $.each(self.ecus(), function(index, element){
        no += element.numberOfStoredDtcs();
      });
      return no;
    });
    self.requestActive = ko.computed(function(){
      isOneRequestActive = false;
      $.each(self.ecus(), function(index, element){
        console.log("checkrequestactive");
        console.log(element.requestActive());
        if (element.requestActive()){
          isOneRequestActive = true;
        }
      });
      return isOneRequestActive;
    });

    // Behaviours
    self.readAllErrorMemories = function(){
        $.each(self.ecus(), function(index, element){
          element.readErrorMemory();
        });
    };
    
    self.goToPage = function(page) {
        self.chosenPageId(page);
    };
    
    self.goToPage('Home');
};

ko.applyBindings(new LeafViewModel());
