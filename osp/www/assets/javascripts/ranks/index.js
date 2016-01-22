

import React from 'react';
import { Provider } from 'react-redux';
import ReactDOM from 'react-dom';

import createStore from './store';
import reducers from './reducers';
import App from './components/app';

import './page';


const store = createStore(reducers);


// Mount the app.
ReactDOM.render(
  <Provider store={store}><App /></Provider>,
  document.getElementById('ranks'),
);
