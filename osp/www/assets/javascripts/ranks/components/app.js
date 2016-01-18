

import React, { Component } from 'react';
import Filters from './filters';
import Results from './results';


export default class extends Component {


  /**
   * Render the application.
   */
  render() {
    return (
      <div className="container">
        <div className="row">

          <div className="col-md-4 hidden-xs hidden-sm">
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
