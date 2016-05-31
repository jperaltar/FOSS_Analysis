(function () {
  'use strict';
  angular.module('charts').directive('chart',
    [function () {
      var link = function (scope, element) {
        var chart;
        scope.$watch('graphData', function (graphData) {
          //Using nvd3 library to create bars chart
          var svg = element.find('svg');

          var update = function() {
            d3.select(svg[0])
              .datum(graphData)
              .call(chart);
          }

          scope.$on('chartinit', update);

          nv.addGraph(function () {
            switch (scope.type) {
              case 'bar':
                chart = nv.models.discreteBarChart()
                  .x(function(d) { return d.label })
                  .y(function(d) { return d.value })
                  .staggerLabels(true)
                  .showValues(false);
                break;
              case 'pie':
                chart = nv.models.pieChart()
                  .x(function(d) { return d.label })
                  .y(function(d) { return d.value })
                  .showLegend(false)
                  .showLabels(false);
                break;
              default:
                chart = nv.models.discreteBarChart();
            }

            nv.utils.windowResize(chart.update);

            scope.$emit('chartinit');
          });
        }, true);

        return chart;
      }

      return {
        restrict: 'E',
        link: link,
        scope: {
          type: '=',
          graphData: '=',
          graphWidth: '=',
          graphHeight: '='
        }
      }
    }
  ]);
})();
