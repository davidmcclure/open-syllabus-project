

import { createReducer } from '../utils';

import {
  CHANGE_CORPUS_FILTER,
  CHANGE_FIELD_FILTER,
} from '../constants';


const initialState = {
  corpus: null,
  field_id: null,
};


const handlers = {

  [CHANGE_CORPUS_FILTER]: (state, action) => ({
    corpus: action.values
  }),

  [CHANGE_FIELD_FILTER]: (state, action) => ({
    field_id: action.values
  })

};


export default createReducer(initialState, handlers);
