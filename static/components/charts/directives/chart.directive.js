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
            if (chart) {
              d3.select(svg[0])
                .attr("width", scope.graphWidth)
                .attr("height", scope.graphHeight)
                .datum(graphData)
                .call(chart);
            }
          }

          scope.$on('chartinit', update);

          function addGraph() {
            nv.addGraph(function () {
              switch (scope.type) {
                case 'bar':
                  graphData = [{
                    key: 'Cumulative Return',
                    values: graphData
                  }];
                  chart = nv.models.discreteBarChart()
                    .x(function(d) { return d.label })
                    .y(function(d) { return d.value })
                    .staggerLabels(true)
                    .showValues(false);
                  scope.$emit('chartinit');
                  break;
                case 'pie':
                  chart = nv.models.pieChart()
                    .x(function(d) { return d.label })
                    .y(function(d) { return d.value })
                    .showLegend(true)
                    .showLabels(true)
                    .labelType("percent");
                  scope.$emit('chartinit');
                  break;
              }
            });
          }
          addGraph();
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
