

import React, { Component } from 'react';


export default class extends Component {


  /**
   * Render the application.
   */
  render() {
    return (
      <div className="container">
        <div className="row">

          <div className="col-md-4">
            filters
          </div>

          <div className="col-md-8">
            results
          </div>

        </div>
      </div>
    );
  }


}
