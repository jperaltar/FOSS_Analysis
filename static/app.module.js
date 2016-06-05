(function () {
  'use strict';

  var appName = 'FOSS_Analysis';
  var app = angular.module(appName, ['ngRoute', 'main', 'statistics', 'analysis']);

  app.config(['$locationProvider',
    function ($locationProvider) {
      $locationProvider.html5Mode(true);
    }
  ]);

  app.config(['$httpProvider',
    function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
  ]);
})();
