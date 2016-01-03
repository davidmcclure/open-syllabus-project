

import { createReducer } from '../utils';

import {
  REQUEST_RESULTS,
  RECEIVE_RESULTS,
} from '../constants';


const initialState = {
  loading: false,
  hitCount: 0,
  hits: [],
};


const handlers = {

  [REQUEST_RESULTS]: () => ({
    loading: true,
  }),

  [RECEIVE_RESULTS]: (state, action) => ({
    loading: false,
    hitCount: action.results.total,
    hits: action.results.hits,
  }),

};


export default createReducer(initialState, handlers);
