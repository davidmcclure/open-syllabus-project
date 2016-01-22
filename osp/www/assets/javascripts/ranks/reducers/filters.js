

import { createReducer } from '../utils';

import {
  CHANGE_FILTERS,
  LOAD_NEXT_PAGE,
  CLEAR_FILTERS,
} from '../constants';


const initialState = {

  query: '',

  corpus: [],
  field_id: [],
  institution_id: [],
  state: [],
  country: [],

  page: 1,

};


const handlers = {

  [CHANGE_FILTERS]: (state, action) => {
    return action.filters;
  },

  [LOAD_NEXT_PAGE]: (state) => {
    return {
      page: state.page + 1
    };
  },

  [CLEAR_FILTERS]: () => (initialState),

};


export default createReducer(initialState, handlers);
