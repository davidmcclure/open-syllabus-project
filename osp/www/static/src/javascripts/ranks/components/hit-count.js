

import React, { Component } from 'react';
import { connect } from 'react-redux';


@connect(state => state.results)
export default class extends Component {


  /**
   * Render the hit counter.
   */
  render() {

    let content;

    // TODO: Spinkit?
    // Initial state.
    if (!this.props.totalHits) {
      content = <span>Loading...</span>;
    }

    else {

      // Format the value.
      let totalHits = this.props.totalHits.toLocaleString();

      content = (
        <span>
          <span className="count">{totalHits}</span>{' '}
          <span className="texts">texts</span>
        </span>
      )

    }

    return (
      <div id="hit-count">
        {content}
      </div>
    );

  }


}
