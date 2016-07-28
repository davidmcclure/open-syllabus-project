

import _ from 'lodash';
import queryString from 'query-string';


/**
 * Map action types to handlers.
 *
 * @param {Object} initialState
 * @param {Object} handlers
 */
export function createReducer(initialState, handlers) {
  return (state = initialState, action) => {

    // If a handler is provided for the current action, apply the reducer
    // and merge the result with the initial state.

    if (_.has(handlers, action.type)) {
      return {
        ...state,
        ...handlers[action.type](state, action),
      };
    }

    // Otherwise, return the intial state.

    else {
      return state;
    }

  };
}


/**
 * Build a querystring for the ranks API from a params object.
 *
 * @param {Object} params
 * @return {String}
 */
export function makeQueryString(params) {

  // Filter out empty values.
  let pruned = _.pickBy(params, function(v) {
    return !_.includes([[], null, ''], v);
  });

  return queryString.stringify(pruned);

}


/**
 * Parse the search string on the URL.
 *
 * @return {String}
 */
export function parseWindowSearch() {

  let params = queryString.parse(window.location.search);

  return _.mapValues(params, function(v) {

    // Cast numerics -> numbers.
    if (!isNaN(v)) {
      v = Number(v);
    }

    // Ensure values are arrays.
    return !_.isArray(v) ? [v] : v;

  });

}
