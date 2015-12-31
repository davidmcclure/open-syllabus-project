

import { createReducer } from '../utils';

import {
  CHANGE_CORPUS_FILTER,
  CHANGE_FIELD_FILTER,
  CHANGE_SUBFIELD_FILTER,
  CHANGE_INSTITUTION_FILTER,
  CHANGE_STATE_FILTER,
  CHANGE_COUNTRY_FILTER,
} from '../constants';


const initialState = {
  corpus: null,
  field_id: null,
  subfield_id: null,
  institution_id: null,
  state: null,
  country: null,
};


const handlers = {

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

};


export default createReducer(initialState, handlers);
