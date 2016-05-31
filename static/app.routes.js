angular.module('FOSS_Analysis').config(['$routeProvider',
  function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: '/static/components/main/partials/mainWrapper.html',
        controller: 'MainController'
      });
  }
]);
