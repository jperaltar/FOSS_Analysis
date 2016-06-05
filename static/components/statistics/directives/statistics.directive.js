(function () {
  'use strict';
  angular.module('statistics').directive('statistics', function () {
    return {
      restrict: 'E',
      templateUrl: '/static/components/statistics/partials/statistics.html'
    };
  });
})();
