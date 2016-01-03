

import React, { Component } from 'react';
import { connect } from 'react-redux';


@connect(state => state.results)
export default class extends Component {


  /**
   * Render the hit counter.
   */
  render() {

    let content;

    // Initial state.
    if (this.props.loading) {
      content = <span>Loading...</span>;
    }

    // No results.
    else if (this.props.hitCount == 0) {
      content = <span>No results</span>;
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
