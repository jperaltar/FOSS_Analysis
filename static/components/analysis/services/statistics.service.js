(function () {
  'use strict';
  angular.module('analysis')
    .factory('StatisticsService', [
      function () {
        var service = {};

        service.addContributions = function (contributors, file) {
          for (var author in file.authors) {
            for (var i = 0; i < contributors.length; i++) {
              if (contributors[i].label == author) {
                contributors[i].value += file.authors[author]['lines'];
                break;
              }
            }
            if (i > (contributors.length - 1)) {
              var authorObj = {
                'label': author,
                'value': file.authors[author]['lines']
              };
              contributors.push(authorObj);
            }
          }
          return contributors;
        }

        service.addLicenses = function (licenses, file) {
          for (var i = 0; i < file.licenses.length; i++) {
            for (var j = 0; j < licenses.length; j++) {
              if (licenses[j].label == file.licenses[i].short_name) {
                licenses[j].value += 1;
                break;
              }
            }
            if (j > (licenses.length - 1)) {
              var license = {
                'label': file.licenses[i].short_name,
                'value': 1
              };
              licenses.push(license);
            }
          }
          return licenses;
        }

        service.addCopyrights = function (copyrights, file) {
          for (var i = 0; i < file.copyrights.length; i++) {
            for (var j = 0; j < copyrights.length; j++) {
              if (copyrights[j].label == file.copyrights[i][0]) {
                copyrights[j].value += 1;
                break;
              }
            }
            if (j > (copyrights.length - 1)) {
              var copyright = {
                'label': file.copyrights[i][0],
                'value': 1
              };
              copyrights.push(copyright);
            }
          }
          return copyrights;
        }

        return service;
      }
    ]);
})();
