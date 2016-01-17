

import React, { Component } from 'react';
import Filters from './filters';
import Results from './results';
import Router from './router';


export default class extends Component {


  /**
   * Render the application.
   */
  render() {
    return (
      <div className="container">
        <div className="row">

          <Router />

          <div className="col-md-4">
            <Filters />
          </div>

          <div className="col-md-8">
            <Results />
          </div>

        </div>
      </div>
    );
  }


}
