

import { createReducer } from '../utils';

import {
  CHANGE_FILTERS,
  CLEAR_FILTERS,
} from '../constants';


const initialState = {

  query: '',

  corpus: [],
  field_id: [],
  institution_id: [],
  state: [],
  country: [],

};


const handlers = {

  [CHANGE_FILTERS]: (state, action) => (action.filters),

  [CLEAR_FILTERS]: () => (initialState),

};


export default createReducer(initialState, handlers);
