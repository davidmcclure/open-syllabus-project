

import React, { Component } from 'react';
import { connect } from 'react-redux';


@connect(state => state.results)
export default class extends Component {


  /**
   * Render the "Clear Filters" button.
   */
  render() {

    return (
      <div id="clear-filters">
        <p>Clear Filters</p>
      </div>
    );

  }


}
