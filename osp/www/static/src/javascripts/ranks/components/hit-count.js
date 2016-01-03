

import React, { Component } from 'react';
import { connect } from 'react-redux';


@connect(state => ({
  totalHits: state.results.totalHits
}))
export default class extends Component {


  /**
   * Render the hit counter.
   */
  render() {

    // Format the value.
    let totalHits = this.props.totalHits.toLocaleString();

    return (
      <div id="hit-count">
        <span className="count">{totalHits}</span>{' '}
        <span className="texts">texts</span>
      </div>
    );

  }


}
