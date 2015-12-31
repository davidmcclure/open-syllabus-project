

import {
  CHANGE_CORPUS_FILTER,
  CHANGE_FIELD_FILTER,
} from '../constants';


/**
 * When the corpus filter is changed.
 *
 * @param {Mixed} values
 */
export function changeCorpusFilter(values) {
  return {
    type: CHANGE_CORPUS_FILTER,
    values,
  };
}


/**
 * When the field filter is changed.
 *
 * @param {Mixed} values
 */
export function changeFieldFilter(values) {
  return {
    type: CHANGE_FIELD_FILTER,
    values,
  };
}
