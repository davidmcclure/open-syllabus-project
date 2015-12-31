

import { createReducer } from '../utils';

import {
  CHANGE_CORPUS_FILTER,
  CHANGE_FIELD_FILTER,
} from '../constants';


const initialState = {
  filters: {},
  query: null,
};


const handlers = {

  [CHANGE_CORPUS_FILTER]: (state, action) => ({
    filters: {
      corpus: action.values
    }
  }),

  [CHANGE_FIELD_FILTER]: (state, action) => ({
    filters: {
      field_id: action.values
    }
  })

};


export default createReducer(initialState, handlers);
