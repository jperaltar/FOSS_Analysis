(function () {
  'use strict';
  angular.module('statistics').directive('legaldata', function () {
    return {
      restrict: 'E',
      templateUrl: '/static/components/statistics/partials/legal-data.html'
    };
  });
})();
