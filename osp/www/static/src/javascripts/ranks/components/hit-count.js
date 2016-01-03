

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
    if (!this.props.hitCount) {
      content = <span>Loading...</span>;
    }

    else {

      // Format the value.
      let hitCount = this.props.hitCount.toLocaleString();

      content = (
        <span>
          <span className="count">{hitCount}</span>{' '}
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
