(function () {
  'use strict';

  angular.module('FOSS_Analysis').directive('navbar', function () {
    return {
      restrict: 'E',
      templateUrl: '/static/components/navbar/partials/navbar.html'
    };
  });
})();
