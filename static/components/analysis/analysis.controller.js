(function () {
  'use strict';
  angular.module('analysis')
    .controller('AnalysisController', ['$scope', 'AnalysisService', 'StatisticsService',
      function ($scope, AnalysisService, StatisticsService) {
        $scope.contributors = [];
        $scope.licenses = [];
        $scope.copyrights = [];
        $scope.owner = '';
        $scope.url = '';
        $scope.num_files = 0;
        $scope.files = {};

        this.analyze = function () {
          AnalysisService.analyze(this.url)
            .then(function (data) {
              $scope.files = data['files'];
              $scope.owner = data['owner'];
              $scope.url = data['url'];
              $scope.num_files = data['num_files'];
              var auxContrib = [];
              var auxLicenses = [];
              var auxCopyrights = [];
              for (var file in data['files']) {
                auxContrib = StatisticsService.addContributions(auxContrib, data['files'][file]);
                auxLicenses = StatisticsService.addLicenses(auxLicenses, data['files'][file]);
                auxCopyrights = StatisticsService.addCopyrights(auxCopyrights, data['files'][file]);
              }
              $scope.contributors = getDataFormat(auxContrib);
              $scope.licenses = auxLicenses;
              $scope.copyrights = auxCopyrights;
            })
            .catch(function (err) {
              console.log(err);
            });
        }

        function getDataFormat(data) {
          return [{
            key: 'Cumulative Return',
            values: data
          }];
        }
      }
    ]);
})();
