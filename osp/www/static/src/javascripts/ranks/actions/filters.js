

import {
  CHANGE_CORPUS_FILTER,
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
