(function () {
    'use strict';
}());

angular.module('agSADCeFarms')

.controller('todo', function($scope,$http, $uibModal,$log,addTodo,Gettodo,postFactory,updateFactory,modalService,modalMessageService) {
   $scope.selectRow = 0;


//get thetodolist here using resource service
   var entries = Gettodo.gettodo().query()
                  .$promise.then(
                    function(response){
                        $scope.lists = response;
                        console.log("response is ", response);
                    },
                    function(response) {
                        $log.debug("ERROR GETTING TODOITEM:", response);
                        if ( response.data === '{ "error": "Bad Request UE" }' ) {
                            modalMessageService.showMessage( "Error:", "Check the service");
                        } else {
                            modalMessageService.showMessage( "Error:", "An error occurred. ");
                        }
                        $log.debug("Error: "+response.status + " " + response.statusText);

                    }

                 );
   $scope.setClickedRow = function(index){

      $scope.selectedRow = index;
      $scope.selectedFormData = $scope.lists[index];
      $scope.displayForm = true;
   }
    $scope.setRow = function(index){

      $scope.setRow = index;
      $scope.selectedForm = $scope.lists[index];
   }
   $scope.displayForm  = false;

            //rough draft for the code
            //modal instance for thetodoitems
           $scope.openModal = function(index) {
            $scope.add_todo = addTodo.todo();
             var modalInstance = $uibModal.open({
                templateUrl:'views/authadmin/newmodal.html',
                controller:'ModalInstanceCtrl',
                resolve: {
                                    items: function () {
                                        return $scope.selectedFormData.todo_list_json[index];
                                    },
                                    ind: function(){
                                        return $scope.selectedFormData.todo_list_json;
                                    },
                                    addto: function () {
                                        return $scope.add_todo;
                                    },
                                }
              });


             modalInstance.result.then(function (modalResponse) {
                        console.log("modalResponse", modalResponse);
                        console.log("indexhere", $scope.selectedFormData.todo_list_json);
                        console.log("formdata:", $scope.selectedFormData);
                        $scope.selectedFormData.todo_list_json.push(modalResponse)
                    }, function () {
                                $log.debug("cancelled the todo entry");
                    });

               $scope.isDisabled = false;
};
$scope.isDisabled = true;
 $scope.removeRow = function(todo_item_title){
        var index = -1;
        var comArr = eval($scope.selectedFormData.todo_list_json);
        for(var i = 0; i < comArr.length;i++){
          if(comArr[i].todo_item_title == todo_item_title){
                    index = -1;
                    $scope.isDisabled = false;
                    break;
        }
   }

    if (index==-1){
          alert("something gone wrong")
        }
        $scope.selectedFormData.todo_list_json.splice(index,1);

    };
  $scope.ok = function(){
    updateFactory.updateList().update($scope.selectedFormData)
                   .$promise.then(
                   function(response){
                      console.log(response);
                   },
                   function(response) {
                        $log.debug("ERROR ADDING TODOITEM:", response);
                        if ( response.data === '{ "error": "Bad Request UE" }' ) {
                            modalMessageService.showMessage( "Error:", "parameters not set correct");
                        } else {
                            modalMessageService.showMessage( "Error:", "An error occurred. ");
                        }
                        $log.debug("Error: "+response.status + " " + response.statusText);
                    }
                );
   }
})

.controller('ModalInstanceCtrl', function($scope,$log, $uibModalInstance,addTodo,ind, items,addto,postFactory,updateFactory,modalService,modalMessageService){
  $scope.items = items;

//  console.log(items)
  $scope.close = function(){

        $uibModalInstance.dismiss();


    }

       console.log("items", items);
       console.log('itemswithindex',ind);


    $scope.removeRow = function(todo_item_title){
            var index=-1;
            var comArr = eval($scope.selectedFormData.todo_list_json);
            for (var i = 0; i < comArr.length;i++){
                if(comArr[i].todo_item_title == todo_item_title){
                    index = -1;
                    break;
                }
            }
            if (index == -1){
                alert("Removed the row")
            }
            $scope.selectedFormData.todo_list_json.splice(index,1);
    }
    //post the new todolist items here
    $scope.submit = function(){

                          var response = {"todo_item_title":$scope.items.todo_item_title,'todo_item_desc':$scope.items.todo_item_desc}
                        $uibModalInstance.close(response);
                    };


    //update the existing
//    $scope.updateList = function(){
//    updateFactory.updateList().update(items[index].id)
//    updateFactory.updateList().update({})
//                   .$promise.then(
//                   function(response){
//                      console.log(response);
//                   },
//                   function(response) {
//                        $log.debug("ERROR UPDATING TODOITEM:", response);
//                        if ( response.data === '{ "error": "Bad Request UE" }' ) {
//                            modalMessageService.showMessage( "Error:", "parameters not set correct");
//                        } else {
//                            modalMessageService.showMessage( "Error:", "An error occurred. ");
//                        }
//                        $log.debug("Error: "+response.status + " " + response.statusText);
//
//                    }
//                );
//
//        $uibModalInstance.close();
//  }

});

;