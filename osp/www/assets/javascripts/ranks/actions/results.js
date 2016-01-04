

import _ from 'lodash';
import $ from 'jquery';

import { makeQueryString } from '../utils'


import {
  REQUEST_RESULTS,
  RECEIVE_RESULTS,
} from '../constants';


/**
 * Query for results.
 *
 * @param {Object} params
 */
export function loadResults(params) {

  let qs = makeQueryString(params);

  return function(dispatch) {

    // Notify start.
    dispatch(requestResults());

    $.getJSON('/api/ranks', qs, function(json) {
      dispatch(receiveResults(json));
    });

  };

}


/**
 * When results are requested.
 */
function requestResults() {
  return {
    type: REQUEST_RESULTS,
  };
}


/**
 * When results are loaded.
 *
 * @param {Object} json
 */
function receiveResults(results) {
  return {
    type: RECEIVE_RESULTS,
    results,
  };
}
