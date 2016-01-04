

import { combineReducers } from 'redux';

import filters from './filters';
import results from './results';


export default combineReducers({
  filters,
  results,
});
