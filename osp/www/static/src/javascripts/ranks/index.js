

import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from './components/app';


ReactDOM.render(
  <Provider><App /></Provider>,
  document.getElementById('ranks'),
);
