

import _ from 'lodash';
import { createReducer } from '../utils';

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


const initialState = {

  query: '',

  corpus: [],
  field_id: [],
  subfield_id: [],
  institution_id: [],
  state: [],
  country: [],

};


const handlers = {

  [CHANGE_SEARCH_QUERY]: (state, action) => ({
    query: action.query.trim()
  }),

  [CHANGE_CORPUS_FILTER]: (state, action) => ({
    corpus: action.values
  }),

  [CHANGE_FIELD_FILTER]: (state, action) => ({
    field_id: action.values
  }),

  [CHANGE_SUBFIELD_FILTER]: (state, action) => ({
    subfield_id: action.values
  }),

  [CHANGE_INSTITUTION_FILTER]: (state, action) => ({
    institution_id: action.values
  }),

  [CHANGE_STATE_FILTER]: (state, action) => ({
    state: action.values
  }),

  [CHANGE_COUNTRY_FILTER]: (state, action) => ({
    country: action.values
  }),

  [CHANGE_FILTERS]: (state, action) => {

    return _.object(_.map(action.filters, function(val, key) {

      // Array-ify bare values.
      if (key != 'query' && !_.isArray(val)) {
        val = [val];
      }

      return [key, val];

    }));

  },

  [CLEAR_FILTERS]: () => (initialState),

};


export default createReducer(initialState, handlers);
