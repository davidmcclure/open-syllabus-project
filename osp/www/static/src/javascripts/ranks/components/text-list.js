

import _ from 'lodash';
import React, { Component, PropTypes } from 'react';

import TextRow from './text-row';


export default class extends Component {


  static propTypes = {
    totalHits: PropTypes.number.isRequired,
    hits: PropTypes.array.isRequired,
  }


  /**
   * Render the ranking table.
   */
  render() {

    // Format the count.
    let totalHits = this.props.totalHits.toLocaleString();

    // Build the text list.
    let rows = _.map(this.props.hits, function(h, i) {
      return <TextRow key={h._id} hit={h} rank={i+1} />
    });

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
