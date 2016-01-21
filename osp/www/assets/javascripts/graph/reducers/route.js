

import { createReducer } from '../utils';

import {
  CHANGE_ROUTE,
} from '../constants';


const initialState = {
  x: null,
  y: null,
  z: null,
};


const handlers = {

  [CHANGE_ROUTE]: (state, action) => action

};


export default createReducer(initialState, handlers);
