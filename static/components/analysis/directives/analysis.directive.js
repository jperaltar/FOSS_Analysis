(function () {
  'use strict';
  angular.module('analysis').directive('analysis', function () {
    return {
      restrict: 'E',
      templateUrl: '/static/components/analysis/partials/analysis.html'
    };
  });
})();
