(function () {
  'use strict';
  angular.module('analysis')
    .factory('AnalysisService', ['$http', '$q',
      function ($http, $q) {
        var service = {};

        service.analyze = function (url) {
          var deferred = $q.defer();
          $http({
            method: 'POST',
            url: '/analyze',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            data: {
              url: url
            }
          }).success(function (response) {
            console.log('SUCCESS');
            deferred.resolve(response);
          }).error(function (err) {
            console.log('ERROR');
            deferred.reject(err);
          });
          return deferred.promise;
        }
        return service;
      }
    ]);
})();
