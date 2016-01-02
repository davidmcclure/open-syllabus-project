

import _ from 'lodash';
import Qs from 'qs';


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
 * Build an /api/ranks querystring from a filters object.
 *
 * @param {Object} params
 * @return {String}
 */
export function makeQueryString(params) {

  // Filter out empty values.
  let pruned = _.pick(params, function(v) {
    return !_.isEmpty(v);
  });

  return Qs.stringify(pruned, {
    indices: false
  });

}
