(function () {
  'use strict';
  angular.module('statistics')
    .controller('StatisticsController', ['$scope', 'ApiService', 'FormatService',
      function ($scope, ApiService, FormatService) {
        $scope.contributors = [];
        $scope.licenses = [];
        $scope.copyrights = [];
        $scope.languages = [];
        $scope.ownedProjects = [];
        $scope.collaborations = [];
        $scope.selectedInfo = '';
        $scope.user = '';

        this.infoIsSelected = function (info) {
          return ($scope.selectedInfo === info);
        }

        this.getAll = function () {
          $scope.contributors = [];
          $scope.licenses = [];
          $scope.copyrights = [];
          $scope.languages = [];
          $scope.projects = [];

          ApiService.post('/all', {})
            .then(function (response) {
              $scope.selectedInfo = '';
              FormatService.sortData(response['contributors'])
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


              FormatService.sortData(response['licenses'])
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

              FormatService.sortData(response['copyrights'])
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

              FormatService.sortData(response['languages'])
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

              $scope.selectedInfo = 'all';
            })
            .catch(function (err) {
              console.log(err);
            });
        }

        this.getByUser = function () {
          $scope.contributors = [];
          $scope.licenses = [];
          $scope.copyrights = [];
          $scope.languages = [];
          $scope.projects = [];
          $scope.user = this.user;

          ApiService.post('/user', {user: this.user})
            .then(function (response) {
              $scope.selectedInfo = '';
              FormatService.sortData(response['languages'])
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

              $scope.ownedProjects = response['projects']['owned'];
              $scope.collaborations = response['projects']['collaborations'];

              FormatService.sortData(response['licenses'])
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

              FormatService.sortData(response['copyrights'])
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

              $scope.selectedInfo = 'user';
            })
            .catch(function (err) {
              console.log(err);
            });
        }

        this.getByLegalInfo = function () {
          ApiService.post('/legal', {
            license: this.license || '',
            copyright: this.copyright || ''
          })
            .then(function (response) {
              $scope.selectedInfo = '';
              $scope.files = response['files'];
              $scope.selectedInfo = 'legal';
            })
            .catch(function (err) {
              console.log(err);
            });
        }
      }
    ]);
})();
