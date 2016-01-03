

import { createReducer } from '../utils';

import {
  REQUEST_RESULTS,
  RECEIVE_RESULTS,
} from '../constants';


const initialState = {
  loading: false,
  totalHits: null,
  hits: [],
};


const handlers = {

  [REQUEST_RESULTS]: () => ({
    loading: true,
  }),

  [RECEIVE_RESULTS]: (state, action) => ({
    loading: false,
    totalHits: action.results.total,
    hits: action.results.hits,
  }),

};


export default createReducer(initialState, handlers);
