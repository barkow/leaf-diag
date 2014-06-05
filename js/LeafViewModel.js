function EcuViewModel(id){
  var self = this;
  self.id = id;
  self.name = ko.observable();
  self.canClearErrorMemory = ko.observable(false);
  self.storedDtcs = ko.observableArray();
  self.numberOfStoredDtcs = ko.observable(0);
  self.commFailure = ko.observable(false);
  
  self.readErrorMemory = function(){
    console.log("Read Error Memory of " + self.name());
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
    });
    
  };
  
  self.clearErrorMemory = function(){
    console.log("Clear Error Memory of " + self.name());
    $.ajax({
      url: "ecus/"+self.id+"/errormemory", 
      type: "DELETE"
    })    
    .done(function(data){
      self.commFailure(false);
    })
    .fail(function(){
      self.commFailure(true);
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
      new EcuViewModel("ecu2")
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
