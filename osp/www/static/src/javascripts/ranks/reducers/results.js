

import { createReducer } from '../utils';

import {
  REQUEST_RESULTS,
  RECEIVE_RESULTS,
} from '../constants';


const initialState = {
  loading: false,
  total_hits: null,
  hits: [],
};


const handlers = {

  [REQUEST_RESULTS]: () => ({
    loading: true,
  }),

  [RECEIVE_RESULTS]: (state, action) => ({
    loading: false,
    total_hits: action.total,
    hits: action.hits,
  }),

};


export default createReducer(initialState, handlers);
