

import _ from 'lodash';
import classNames from 'classnames';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';

import TextRow from './text-row';
import SKCircle from './sk-circle';


@connect(state => state.results)
export default class extends Component {


  /**
   * Render the ranking table.
   */
  render() {

    // Build the text list.
    let rows = _.map(this.props.hits, function(h, i) {
      return <TextRow key={h._id} hit={h} rank={i+1} />
    });

    // Show a loading spinner.
    let spinner = this.props.loading ? (
      <div className="spinner"><SKCircle /></div>
    ) : null;

    // Table classes.
    let tableCx = classNames('table', 'table-hover', {
      loading: this.props.loading,
    });

    return (
      <div id="text-list">

        <table className={tableCx}>

          <thead>
            <tr>
              <th>Rank</th>
              <th>Count</th>
              <th>Text</th>
            </tr>
          </thead>

          <tbody>
            {rows}
          </tbody>

        </table>

        {spinner}

      </div>
    );

  }


}
