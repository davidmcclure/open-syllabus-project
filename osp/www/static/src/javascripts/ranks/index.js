

import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore } from 'redux';

import reducers from './reducers';
import App from './components/app';


const store = createStore(reducers);


// Mount the app.
ReactDOM.render(
  <Provider store={store}><App /></Provider>,
  document.getElementById('ranks'),
);
