(function () {
  'use strict';
  angular.module('statistics')
    .controller('StatisticsController', ['$scope', 'ApiService',
      function ($scope, ApiService) {
        $scope.contributors = [];
        $scope.licenses = [];
        $scope.copyrights = [];
        $scope.languages = [];
        $scope.projects = [];
        $scope.selectedInfo = '';

        this.infoIsSelected = function (info) {
          return ($scope.selectedInfo === info);
        }

        this.getAll = function () {
          ApiService.post('/all', {})
            .then(function (response) {
              $scope.contributors = response['contributors'];
              $scope.licenses = response['licenses'];
              $scope.copyrights = response['copyrights'];
              $scope.languages = response['languages'];
              $scope.selectedInfo = 'all';
            })
            .catch(function (err) {
              console.log(err);
            });
        }

        this.getByUser = function () {
          ApiService.post('/user', {user: this.user})
            .then(function (response) {
              $scope.languages = response['languages'];
              $scope.projects = response['projects'];
              $scope.licenses = response['licenses'];
              $scope.copyrights = response['copyrights'];
              $scope.selectedInfo = 'user';
            })
            .catch(function (err) {
              console.log(err);
            });
        }

        this.getByLegalInfo = function () {
          ApiService.post('/legal', {license: this.license, copyright: this.copyright})
            .then(function (response) {
              $scope.licenseOwners = response['owners'];
              $scope.licensedFiles = response['licensedFiles'];
              $scope.copyrightsFiles = response['copyrightsFiles'];
            })
        }
      }
    ]);
})();
