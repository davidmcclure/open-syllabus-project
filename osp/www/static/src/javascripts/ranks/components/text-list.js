

import React, { Component, PropTypes } from 'react';


export default class extends Component {


  static propTypes = {
    totalHits: PropTypes.number.isRequired,
    hits: PropTypes.array.isRequired,
  }


  /**
   * Render ranking results.
   */
  render() {

    let totalHits = this.props.totalHits.toLocaleString();

    return (
      <div id="text-list">

        <div className="total-hits">
          <span className="count">{totalHits}</span>{' '}
          <span className="texts">texts</span>
        </div>

      </div>
    );

  }


}
