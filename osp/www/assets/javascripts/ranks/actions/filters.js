

import {

  CHANGE_SEARCH_QUERY,
  CHANGE_CORPUS_FILTER,
  CHANGE_FIELD_FILTER,
  CHANGE_SUBFIELD_FILTER,
  CHANGE_INSTITUTION_FILTER,
  CHANGE_STATE_FILTER,
  CHANGE_COUNTRY_FILTER,

  CHANGE_FILTERS,
  CLEAR_FILTERS,

} from '../constants';


/**
 * When the search query is changed.
 *
 * @param {String|null} query
 */
export function changeSearchQuery(query) {
  return {
    type: CHANGE_SEARCH_QUERY,
    query,
  };
}


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


/**
 * When the subfield filter is changed.
 *
 * @param {Mixed} values
 */
export function changeSubfieldFilter(values) {
  return {
    type: CHANGE_SUBFIELD_FILTER,
    values,
  };
}


/**
 * When the institution filter is changed.
 *
 * @param {Mixed} values
 */
export function changeInstitutionFilter(values) {
  return {
    type: CHANGE_INSTITUTION_FILTER,
    values,
  };
}


/**
 * When the state filter is changed.
 *
 * @param {Mixed} values
 */
export function changeStateFilter(values) {
  return {
    type: CHANGE_STATE_FILTER,
    values,
  };
}


/**
 * When the country filter is changed.
 *
 * @param {Mixed} values
 */
export function changeCountryFilter(values) {
  return {
    type: CHANGE_COUNTRY_FILTER,
    values,
  };
}


/**
 * Apply new values.
 *
 * @param {Object} filters
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
