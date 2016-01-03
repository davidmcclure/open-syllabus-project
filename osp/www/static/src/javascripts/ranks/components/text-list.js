

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

    let rows = null;

    return (
      <div id="text-list">

        <div className="total-hits">
          <span className="count">{totalHits}</span>{' '}
          <span className="texts">texts</span>
        </div>

        <table className="table table-hover">
          <thead>
            <th>Rank</th>
            <th>Count</th>
            <th>Text</th>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>

      </div>
    );

  }


}
