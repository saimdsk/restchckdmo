  (function () {
    'use strict';
}());

angular.module('agSADCeFarms')
    .constant("baseURL", "/AG_SADCeFarms/")

    .factory('listsvc',function($http){
			var svc = {

				getlist:function(){
					return $http({
					    method: 'GET',
					    url:'http://127.0.0.1/AG_SADCeFarms/gettodolist',
                        responseType: 'json',

                    });
			    },
			    postList:function(data){
						return $http.post('http://127.0.0.1/AG_SADCeFarms/todolistupdate', data);

				},
				updateList:function(){
						return $http.put('http://127.0.0.1/AG_SADCeFarms/todolistupdate/43B6AC29-FC9F-E00F-E053-0A54960A8401');

				},
				deleteList:function(){
					return $http.delete('http://127.0.0.1/AG_SADCeFarms/todolistupdate/43B6AC2A-0081-E00F-E053-0A54960A8401');

				}
		};

		return svc;
});