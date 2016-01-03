

import React, { Component } from 'react';
import { connect } from 'react-redux';
import classNames from 'classnames';


@connect(state => state.results)
export default class extends Component {


  /**
   * Render the hit counter.
   */
  render() {

    let content;

    // Loading.
    if (this.props.loading) {
      content = <span>Loading...</span>;
    }

    // No results.
    else if (this.props.hitCount == 0) {
      content = <span>No results</span>;
    }

    // Results.
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

    let cx = classNames({
      loading: this.props.loading,
    });

    return (
      <div id="hit-count" className={cx}>
        {content}
      </div>
    );

  }


}
