

import _ from 'lodash';


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
 * Given an array of select options, extract an individual value (if just one
 * option is selected) or an array of values.
 *
 * @param {Array} options
 */
export function parseFilterValues(options) {
  let values = _.pluck(options, 'value');
  return values.length == 1 ? values[0] : values;
}
