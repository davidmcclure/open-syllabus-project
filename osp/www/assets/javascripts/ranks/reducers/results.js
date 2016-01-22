

import _ from 'lodash';
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

  [RECEIVE_RESULTS]: (state, action) => {

    // If page > 1, add new hits to existing hits.
    let hits = action.params.page > 1 ?
      _.concat(state.hits, action.results.hits) :
      action.results.hits

    return {
      loading: false,
      hitCount: action.results.total,
      hits,
    }

  },

};


export default createReducer(initialState, handlers);
