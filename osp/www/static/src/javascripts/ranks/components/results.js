

import React, { Component } from 'react';
import { connect } from 'react-redux';


@connect(
  state => ({
    results: state.results,
  }),
)
export default class extends Component {


  /**
   * Render the ranking results.
   */
  render() {
    return (
      <div id="results">
        <h1>results</h1>
      </div>
    );
  }


}
