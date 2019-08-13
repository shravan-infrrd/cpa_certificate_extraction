var app=angular.module('docketly-app', []);
//var UI_URL = "http:///54.245.29.69:6789/extract";
//var UI_URL = "http:///localhost:6789/extract";
//var UI_URL ="https://cpa-certificates.infrrdapis.com/find";
//var UI_URL ="http://q.cpa-certificates.infrrdapis.com:4000/find";
//var UI_URL ="http://35.161.218.84:4000/find";
var UI_URL ="http://q.cpa-certificates.infrrdapis.com:4000/find"
//var UI_URL = "http:///localhost:4000/find";

app.controller('DocketlyHomeController', ['$scope','$http',function($scope, $http){
    $scope.extractData=function(){
        $scope.isUploading = true;
        var formData = new FormData(document.querySelector('#upload-form'));
        var uploadUrl = UI_URL;
        $http.post(uploadUrl, formData,{
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined, 'Accept': 'application/json'}
        }).then(
            function successCallback(response) {
                $scope.isUploading = false;
                console.log("----1----")
                console.log(response.data.data)
		console.log(response)
                console.log("----2----")
                $scope.court_info = response.data.data;
                PDFObject.embed(response.data.data['pdf_file_path'], "#pdf-container");
            }, 
            function errorCallback(response) {
                $scope.isUploading = false;
                console.log('response');
            });
    };
}]);


