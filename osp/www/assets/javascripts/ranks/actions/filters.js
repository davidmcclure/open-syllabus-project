

import {
  CHANGE_FILTERS,
  CLEAR_FILTERS,
} from '../constants';


/**
 * Apply new values.
 *
 * @param {Object} filters
 * @param {Boolean} updateRoute
 */
export function changeFilters(filters) {
  return {
    type: CHANGE_FILTERS,
    filters,
  };
}


/**
 * Reset the filters.
 */
export function clearFilters() {
  return {
    type: CLEAR_FILTERS,
  };
}
