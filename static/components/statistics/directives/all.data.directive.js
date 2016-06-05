(function () {
  'use strict';
  angular.module('statistics').directive('alldata', function () {
    return {
      restrict: 'E',
      templateUrl: '/static/components/statistics/partials/all-data.html'
    };
  });
})();
