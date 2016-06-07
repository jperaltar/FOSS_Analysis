(function () {
  angular.module('charts').factory('FormatService', ['$q',
    function ($q) {
      var service = {};

      service.sortData = function (data) {
        var deferred = $q.defer();

        if (data.length > 1) {
          var sortedData = []
          for (var i = 0; i < data.length; i++) {
            if (sortedData.length > 0) {
              for (var j = 0; j < sortedData.length; j++) {
                if (sortedData[j]['value'] < data[i]['value']) {
                  sortedData.splice(j, 0, data[i]);
                  break;
                }
              }
              if (j === sortedData.length) {
                sortedData.push(data[i]);
              }
            } else {
              sortedData.push(data[i]);
            }
          }
          deferred.resolve(sortedData);
        } else {
          deferred.reject(data);
        }
        return deferred.promise;
      }

      service.trimData = function (cutpoint, data) {
        var deferred = $q.defer();

        if (cutpoint < data.length - 1) {
          var trimedData = data.splice(0, cutpoint);
          var others = {'label': 'Others', 'value': 0};
          for (var i = 0; i < data.length; i++) {
            others['value'] = others['value'] + data[i]['value'];
          }
          trimedData.push(others);
          deferred.resolve(trimedData);
        } else {
          deferred.reject(data);
        }
        return deferred.promise;
      }

      return service;
    }
  ])
})();
