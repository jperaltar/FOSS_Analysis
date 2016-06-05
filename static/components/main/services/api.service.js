(function () {
  'use strict';
  angular.module('main')
    .factory('ApiService', ['$http', '$q',
      function ($http, $q) {
        var service = {};

        service.post = function (url, data) {
          console.log(data);
          $('chart > *').remove();
          $('chart').append('<svg></svg>');
          var deferred = $q.defer();
          $http({
            method: 'POST',
            url: url,
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            },
            data: data
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
