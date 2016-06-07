(function() {
  angular.module("main").factory("interceptors", [function() {
    return {
      'request': function(request) {
        if (request.beforeSend) {
          request.beforeSend();
        }
        return request;
      },

      'response': function(response) {
        if (response.config.complete) {
          response.config.complete(response);
        }
        return response;
      }
    };
  }]);
})();
