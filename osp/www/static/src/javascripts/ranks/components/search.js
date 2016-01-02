

import React, { Component } from 'react';


export default class extends Component {


  /**
   * Render the search box.
   */
  render() {
    return (
      <div id="search">

        <input
          className="form-control"
          placeholder="Search texts"
        />

      </div>
    );
  }


}
