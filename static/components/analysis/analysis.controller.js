(function () {
  'use strict';
  angular.module('analysis')
    .controller('AnalysisController', ['$scope', 'ApiService', 'StatisticsService', 'FormatService',
      function ($scope, ApiService, StatisticsService, FormatService) {
        $scope.languages = [];
        $scope.contributors = [];
        $scope.licenses = [];
        $scope.copyrights = [];
        $scope.owner = '';
        $scope.url = '';
        $scope.num_files = 0;
        $scope.files = {};

        this.analyze = function () {
          $scope.languages = [];
          $scope.contributors = [];
          $scope.licenses = [];
          $scope.copyrights = [];
          $scope.owner = '';
          $scope.url = '';
          $scope.num_files = 0;
          ApiService.post('/analyze', {'url': this.url})
            .then(function (data) {
              $scope.files = data['files'];
              $scope.owner = data['owner'];
              $scope.url = data['url'];
              $scope.num_files = data['num_files'];
              var auxContrib = [];
              var auxLicenses = [];
              var auxCopyrights = [];
              var auxLanguages = [];
              for (var file in data['files']) {
                auxContrib = StatisticsService.addContributions(auxContrib, data['files'][file]);
                auxLicenses = StatisticsService.addLicenses(auxLicenses, data['files'][file]);
                auxCopyrights = StatisticsService.addCopyrights(auxCopyrights, data['files'][file]);
                auxLanguages = StatisticsService.addLanguages(auxLanguages, data['files'][file]);
              }

              FormatService.sortData(auxLanguages)
                .then(function (sortedData) {
                  FormatService.trimData(8, sortedData)
                    .then(function (trimedData) {
                      $scope.languages = trimedData;
                    })
                    .catch(function (data) {
                      $scope.languages = data;
                    });
                })
                .catch(function (data) {
                  $scope.languages = data;
                });

              FormatService.sortData(auxContrib)
                .then(function (sortedData) {
                  FormatService.trimData(8, sortedData)
                    .then(function (trimedData) {
                      $scope.contributors = trimedData;
                    })
                    .catch(function (data) {
                      $scope.contributors = data;
                    });
                })
                .catch(function (data) {
                  $scope.contributors = data;
                });

              FormatService.sortData(auxLicenses)
                .then(function (sortedData) {
                  FormatService.trimData(8, sortedData)
                    .then(function (trimedData) {
                      $scope.licenses = trimedData;
                    })
                    .catch(function (data) {
                      $scope.licenses = data;
                    });
                })
                .catch(function (data) {
                  $scope.licenses = data;
                });

              FormatService.sortData(auxCopyrights)
                .then(function (sortedData) {
                  FormatService.trimData(8, sortedData)
                    .then(function (trimedData) {
                      $scope.copyrights = trimedData;
                    })
                    .catch(function (data) {
                      $scope.copyrights = data;
                    });
                })
                .catch(function (data) {
                  $scope.copyrights = data;
                });
            })
            .catch(function (err) {
              console.log(err);
            });
        }
      }
    ]);
})();
