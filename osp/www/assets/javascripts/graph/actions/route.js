

import {
  CHANGE_ROUTE,
} from '../constants';


/**
 * When the route changes.
 *
 * @param {Number} x
 * @param {Number} y
 * @param {Number} z
 */
export function changeFilters(x, y, z) {
  return {
    type: CHANGE_ROUTE,
    x, y, z,
  };
}
