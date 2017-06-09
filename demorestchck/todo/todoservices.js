(function () {
    'use strict';
}());

angular.module('agSADCeFarms')
    //.constant("baseURL", "http://oit-6gsgyv1.oit.state.nj.us/AG_SADCeFarmsWS/")
    .constant("baseURL", "/AG_SADCeFarms/")





    //service for get thetodo List
     .service('Gettodo', ['$resource',function($resource){
        this.gettodo = function(){
        return $resource('http://127.0.0.1/AG_SADCeFarms/gettodolist',{method:'GET'});

    };
    }])

    .service('addTodo', ['$resource', function($resource ) {
        this.todo = function(){
            return {
                "todo_item_desc": "",
                "todo_item_title": "",
            };

        };
    }])
    //service for the Post thetodolist
    .service('postFactory', ['$resource', function($resource) {

        this.postList = function(){

            return $resource('http://127.0.0.1/AG_SADCeFarms/todolistupdate', null, {'save':{method:'POST'}});
        };

    }])
    //service for update thetodolist
    .service('updateFactory', ['$resource', function($resource) {

        this.updateList = function(){

            return $resource('http://127.0.0.1/AG_SADCeFarms/todolistupdate/43B6AC29-FC9F-E00F-E053-0A54960A8401', null, {'update':{method:'PUT'}});
        };

    }])

    .service('modalService', [ '$log', '$uibModal',  function( $log, $uibModal ) {
        var modalDefaults = {
            backdrop: true,
            keyboard: true,
            modalFade: true,
            templateUrl: 'templates/authadmin/modal.html'
        };

        var modalOptions = {
            closeButtonText: 'Close',
            closeButtonVisible: true,
            actionButtonText: 'OK',
            actionButtonVisible: true,
            headerText: 'Proceed?',
            bodyText: 'Perform this action?'
        };

        this.showModal = function (customModalDefaults, customModalOptions, resultToGet ) {
            if (!customModalDefaults) customModalDefaults = {};
            customModalDefaults.backdrop = 'static';
            if (!resultToGet) resultToGet = {};
            $log.debug("in showModal resultToGet:", resultToGet);
            return this.show(customModalDefaults, customModalOptions, resultToGet );
        };

        this.show = function (customModalDefaults, customModalOptions, resultToGet ) {
            //Create temp objects to work with since we're in a singleton service
            var tempModalDefaults = {};
            var tempModalOptions = {};
            var tmpResultToGet = resultToGet;

            //Map angular-ui modal custom defaults to modal defaults defined in service
            angular.extend(tempModalDefaults, modalDefaults, customModalDefaults);

            //Map modal.html $scope custom properties to defaults defined in service
            angular.extend(tempModalOptions, modalOptions, customModalOptions);

            if (!tempModalDefaults.controller) {
                tempModalDefaults.controller = ('TempModalController', ['$scope', '$uibModalInstance',
                    function ($scope, $uibModalInstance, customModalDefaults) {
                        $scope.resultToGet = tmpResultToGet;
                        $scope.modalOptions = tempModalOptions;
                        $scope.modalOptions.ok = function (resultToGet) {
                            $uibModalInstance.close(resultToGet);
                        };
                        $scope.modalOptions.close = function () {
                            $uibModalInstance.dismiss('cancel');
                        };
                }]);
            }
            return $uibModal.open(tempModalDefaults).result;
        };
    }])

    .service('modalMessageService', [ '$log', 'modalService', '$uibModal',  function( $log, modalService, $uibModal ) {
        this.showMessage = function ( heading, message ) {
            var modalOptions = {
                actionButtonText: 'Close',
                closeButtonVisible: false,
                headerText: heading,
                bodyText: message
            };
            modalService.showModal({}, modalOptions, {})
                // We don't care about the response
                .then( function(response){}, function(){});
        };

    }])
;
