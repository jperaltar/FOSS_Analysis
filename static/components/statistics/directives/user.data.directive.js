(function () {
  'use strict';
  angular.module('statistics').directive('userdata', function () {
    return {
      restrict: 'E',
      templateUrl: '/static/components/statistics/partials/user-data.html'
    };
  });
})();
