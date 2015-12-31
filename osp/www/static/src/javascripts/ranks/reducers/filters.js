

import { createReducer } from '../utils';

import {
  CHANGE_CORPUS_FILTER,
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
  })

};


export default createReducer(initialState, handlers);
