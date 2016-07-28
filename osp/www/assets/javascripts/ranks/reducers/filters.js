

import { createReducer, parseWindowSearch } from '../utils';

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

  ...parseWindowSearch()

};


const handlers = {

  [CHANGE_FILTERS]: (state, action) => ({

    ...action.filters,

    // Reset the page offset when the filters change.
    page: 1,

  }),

  [LOAD_NEXT_PAGE]: (state) => ({
      page: state.page + 1
  }),

  [CLEAR_FILTERS]: () => (initialState),

};


export default createReducer(initialState, handlers);
