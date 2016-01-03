

import _ from 'lodash';
import React, { Component } from 'react';
import { connect } from 'react-redux';


@connect(
  state => state.results
)
export default class extends Component {


  /**
   * Render the ranking results.
   */
  render() {

    let content;

    // Loading.
    if (this.props.loading && _.isEmpty(this.props.hits)) {
      content = <h2>Loading...</h2>;
    }

    // No results.
    else if (_.isEmpty(this.props.hits)) {
      content = <h2>No results</h2>;
    }

    // Results.
    else {
      content = <h2>Results</h2>;
    }

    return (
      <div id="results">
        {content}
      </div>
    );

  }


}
