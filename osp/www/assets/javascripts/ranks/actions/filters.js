

import {
  CHANGE_FILTERS,
  LOAD_NEXT_PAGE,
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
 * Increment the page offset.
 */
export function loadNextPage() {
  return {
    type: LOAD_NEXT_PAGE,
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
